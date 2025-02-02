import os
import pathlib

import fitz  # PyMuPDF를 사용
import pymupdf4llm


def pdf_to_markdown(pdf_path, md_path):
    """
    PDF 파일을 읽어서 Markdown 형식으로 저장합니다.
    """
    md_text = pymupdf4llm.to_markdown(pdf_path)
    
    pathlib.Path(md_path).write_bytes(md_text.encode())
    # try:
    #     # PDF 열기
    #     doc = fitz.open(pdf_path)
    #     md_content = []
        
    #     # PDF 페이지 텍스트 추출
    #     for page_num in range(len(doc)):
    #         page = doc.load_page(page_num)
    #         text = page.get_text("text")  # 텍스트만 추출
    #         md_content.append(f"# Page {page_num + 1}\n\n{text}\n\n")
        
    #     # Markdown 파일 저장
    #     with open(md_path, "w", encoding="utf-8") as md_file:
    #         md_file.write("\n".join(md_content))
    #     print(f"변환 완료: {pdf_path} -> {md_path}")
    
    # except Exception as e:
    #     print(f"오류 발생: {pdf_path} 변환 중 {str(e)}")


def process_directory(input_dir, output_dir):
    """
    디렉토리 내부의 모든 PDF 파일을 재귀적으로 탐색하고 변환합니다.
    """
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".pdf"):  # PDF 파일 필터링
                pdf_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_dir)
                output_subdir = os.path.join(output_dir, relative_path)
                os.makedirs(output_subdir, exist_ok=True)
                
                md_filename = os.path.splitext(file)[0] + ".md"
                md_path = os.path.join(output_subdir, md_filename)
                
                pdf_to_markdown(pdf_path, md_path)


if __name__ == "__main__":
    input_directory = input("PDF 파일들이 있는 디렉토리 경로를 입력하세요: ")
    output_directory = input("Markdown 파일을 저장할 디렉토리 경로를 입력하세요: ")

    if not os.path.exists(input_directory):
        print("입력 디렉토리가 존재하지 않습니다.")
    else:
        os.makedirs(output_directory, exist_ok=True)
        process_directory(input_directory, output_directory)
        print(f"모든 PDF 파일이 {output_directory}에 Markdown 형식으로 저장되었습니다.")