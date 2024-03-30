import os
import glob
import markdown
import shutil


def convert_md_to_html(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as md_file:
        md_text = md_file.read()
        html: str = markdown.markdown(
            md_text,
            extensions=["tables", "mdx_math"],
            extension_configs={"mdx_math": {"enable_dollar_delimiter": True}},
        )

    # タイトルの取得
    title: str = None
    for line in md_text.splitlines():
        if line[0] == "#":
            title = line.replace("#", "").strip()
            break
    if title is None:
        title = os.path.splitext(os.path.basename(input_path))[0]

    with open("template.html", "r", encoding="utf-8") as template_file:
        template_text: str = template_file.read()
        html = template_text.replace("{{TITLE}}", title).replace(
            "{{BODY}}", html
        )
        html = html.replace('.md"', '.html"')

    with open(output_path, "w", encoding="utf-8") as html_file:
        html_file.write(html)


def main():
    input_folder = "markdown"
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
    IMAGE_EXTENSIONS = (
        ".gif",
        ".jpg",
        ".png",
        ".svg",
    )
    for image_extension in IMAGE_EXTENSIONS:
        for image_file_path in glob.glob(
            f"{input_folder}/**/*{image_extension}", recursive=True
        ):
            relative_path = os.path.relpath(image_file_path, input_folder)
            output_path = os.path.join(output_folder, relative_path)
            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            shutil.copy2(image_file_path, output_path)
            print(f"コピー完了: {image_file_path} -> {output_path}")


if __name__ == "__main__":
    main()
