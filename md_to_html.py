import os
import glob
import markdown


def convert_md_to_html(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as md_file:
        md_text = md_file.read()
        html = markdown.markdown(md_text)

    with open(output_path, "w", encoding="utf-8") as html_file:
        html_file.write(html)


def main():
    input_folder = "."
    output_folder = "html"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for md_file_path in glob.glob(f"{input_folder}/**/*.md", recursive=True):
        relative_path = os.path.relpath(md_file_path, input_folder)
        output_path = (
            os.path.splitext(os.path.join(output_folder, relative_path))[0]
            + ".html"
        )
        output_dir = os.path.dirname(output_path)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        convert_md_to_html(md_file_path, output_path)
        print(f"変換完了: {md_file_path} -> {output_path}")


if __name__ == "__main__":
    main()
