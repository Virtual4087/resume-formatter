from flask import request, render_template, jsonify, send_file, current_app, make_response, Response
from io import BytesIO
import os
import json
import uuid
from app.services.parser_service import ResumeParser
from app.services.document_service import DocumentGenerator

def register_routes(app):
    """Register all application routes"""
    
    @app.route('/')
    def home():
        """Render the home page"""
        return render_template('index.html')

    @app.route('/submit', methods=['POST'])
    def submit():
        """Process the submitted resume"""
        resume_text = request.form.get('resume')
        selected_model = request.form.get('aiModel', 'gemini-1.5-flash')  # Default to gemini-1.5-flash
        
        if not resume_text or not resume_text.strip():
            return jsonify({"status": "error", "message": "Error: Resume text cannot be empty."}), 400

        try:
            # Get API keys from app config or env
            api_keys = current_app.config.get('GEMINI_API_KEYS')
            if not api_keys:
                api_key = current_app.config.get('GEMINI_API_KEY')
                api_keys = [api_key] if api_key else []
            parser = ResumeParser(api_keys)

            # Use the progress-enabled parser
            progress = []
            final_result = None
            for update in parser.parse_resume_with_progress(resume_text, model=selected_model):
                progress.append(update)
                if update.get("status") == "success":
                    final_result = update["result"]
                    break
                if update.get("error"):
                    break
            if final_result:
                skill_order = list(final_result['technical_skills'].keys())
                return jsonify({
                    "status": "success",
                    "message": "Resume successfully processed.",
                    "data": final_result,
                    "skill_order": skill_order,
                    "model_used": selected_model,
                    "progress": progress
                })
            else:
                return jsonify({
                    "status": "error",
                    "message": progress[-1]["status"] if progress else "Failed to parse resume.",
                    "progress": progress
                }), 500
        except Exception as e:
            return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500

    @app.route('/generate', methods=['POST'])
    def generate_document():
        """Generate and stream a resume document from the edited data"""
        try:
            # Get the updated resume data from the request
            resume_data = request.json
            
            if not resume_data:
                return jsonify({"status": "error", "message": "No resume data provided"}), 400
                
            # Generate a unique file name suggestion based on the user's name
            suggested_filename = f"{resume_data['contact']['name'].replace(' ', '_')}_Resume.docx"
            
            # Create document in memory
            doc_generator = DocumentGenerator()
            output_stream = doc_generator.create_resume_document_stream(resume_data)
            
            # Return the document data as a downloadable file with suggested filename
            response = make_response(output_stream.getvalue())
            response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            response.headers['Content-Disposition'] = f'attachment; filename="{suggested_filename}"'
            
            return response
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route('/generate/pdf', methods=['POST'])
    def generate_pdf():
        """Generate and stream a PDF version of the resume"""
        try:
            # Get the updated resume data from the request
            resume_data = request.json
            
            if not resume_data:
                return jsonify({"status": "error", "message": "No resume data provided"}), 400
            
            # Generate a unique file name suggestion based on the user's name
            suggested_filename = f"{resume_data['contact']['name'].replace(' ', '_')}_Resume.pdf"
                
            # Create document generator
            doc_generator = DocumentGenerator()
            
            # Generate PDF in memory
            pdf_stream = doc_generator.create_pdf_stream(resume_data)
            if not pdf_stream:
                return jsonify({
                    "status": "error", 
                    "message": "PDF conversion requires docx2pdf module and Microsoft Word or LibreOffice."
                }), 500
            
            # IMPORTANT: Reset stream position to beginning
            pdf_stream.seek(0)
            
            # Get the PDF bytes
            pdf_bytes = pdf_stream.getvalue()
            
            # Create response with proper headers
            response = make_response(pdf_bytes)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = f'attachment; filename="{suggested_filename}"'
            response.headers['Content-Length'] = len(pdf_bytes)
            
            return response
            
        except Exception as e:
            print(f"PDF generation error: {str(e)}")  # Add logging
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route('/download/<filename>', methods=['GET'])
    def download_file(filename):
        """Download the generated resume document and clean up temporary files"""
        try:
            # Send the file to the client for download
            response = send_file(filename, as_attachment=True)
            
            # Register a function to clean up the file after it's sent
            @response.call_on_close
            def cleanup():
                try:
                    # Only delete files with temp_ prefix
                    if filename.startswith('temp_') and os.path.exists(filename):
                        os.remove(filename)
                        print(f"Temporary file {filename} deleted after download")
                except Exception as e:
                    print(f"Error cleaning up file: {str(e)}")
                    
            return response
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route('/get_raw_json', methods=['POST'])
    def get_raw_json():
        """Return the raw JSON data from Gemini API parsing"""
        try:
            # Get the parsed resume data from request
            resume_data = request.json
            
            if not resume_data:
                return jsonify({"status": "error", "message": "No data provided"}), 400
            
            # Return the raw JSON data
            return jsonify({
                "status": "success",
                "data": resume_data
            })
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500