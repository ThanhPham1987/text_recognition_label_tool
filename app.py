# import os
# import glob
# import gradio as gr
# from PIL import Image
#
# class ImageLabeler:
#     def __init__(self, image_folder):
#         self.image_folder = image_folder
#         self.image_paths = glob.glob(os.path.join(image_folder, '*.png')) + glob.glob(os.path.join(image_folder, '*.jpg'))
#         self.total_images = len(self.image_paths)
#         self.current_index = 0
#
#     def get_current_image(self):
#         if self.total_images == 0:
#             return None
#         return self.image_paths[self.current_index]
#
#     def get_label_path(self, image_path):
#         return os.path.splitext(image_path)[0] + '.txt'
#
#     def load_image_and_label(self):
#         image_path = self.get_current_image()
#         if not image_path:
#             return None, ""
#         label_path = self.get_label_path(image_path)
#         label = ""
#         if os.path.exists(label_path):
#             with open(label_path, 'r', encoding='utf-8') as f:
#                 label = f.read().strip()
#         return Image.open(image_path), label
#
#     def save_label(self, label_text):
#         image_path = self.get_current_image()
#         if image_path:
#             label_path = self.get_label_path(image_path)
#             with open(label_path, 'w', encoding='utf-8') as f:
#                 if image_path not in label_text:
#                     f.write(f'{image_path}, "{label_text}"\n')
#                 else:
#                     f.write(label_text)
#
#     def next_image(self, label_text):
#         self.save_label(label_text)
#         if self.current_index < self.total_images - 1:
#             self.current_index += 1
#         return self.load_image_and_label(), self.progress()
#
#     def prev_image(self, label_text):
#         self.save_label(label_text)
#         if self.current_index > 0:
#             self.current_index -= 1
#         return self.load_image_and_label(), self.progress()
#
#     def progress(self):
#         return f"{self.current_index + 1}/{self.total_images}"
#
# # Gradio Interface
# def create_gradio_app(folder_path):
#     labeler = ImageLabeler(folder_path)
#
#     with gr.Blocks() as demo:
#         gr.Markdown("## 🏷️ Image Labeling Tool")
#
#         image = gr.Image(type="pil", label="Image")
#         textbox = gr.Textbox(label="Label", placeholder="Enter label for image")
#         progress = gr.Label()
#
#         with gr.Row():
#             prev_button = gr.Button("⬅️ Previous")
#             next_button = gr.Button("➡️ Next")
#
#         def update_prev(label_text):
#             (img, lbl), prog = labeler.prev_image(label_text)
#             return img, lbl, prog
#
#         def update_next(label_text):
#             (img, lbl), prog = labeler.next_image(label_text)
#             return img, lbl, prog
#
#         def load_initial():
#             img, lbl = labeler.load_image_and_label()
#             return img, lbl, labeler.progress()
#
#         prev_button.click(update_prev, inputs=[textbox], outputs=[image, textbox, progress])
#         next_button.click(update_next, inputs=[textbox], outputs=[image, textbox, progress])
#         demo.load(fn=load_initial, inputs=[], outputs=[image, textbox, progress])
#
#     return demo
#
# # Run
# if __name__ == '__main__':
#     import argparse
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-f', '--input_dir', type=str, required=True, help='Path to image folder')
#     args = parser.parse_args()
#
#     app = create_gradio_app(args.input_dir)
#     app.launch()
#
import os
import glob
import gradio as gr
from PIL import Image

class ImageLabeler:
    def __init__(self, image_folder):
        self.image_folder = image_folder
        self.image_paths = glob.glob(os.path.join(image_folder, '*.png')) + glob.glob(os.path.join(image_folder, '*.jpg'))
        self.total_images = len(self.image_paths)
        self.current_index = 0

    def get_current_image(self):
        if self.total_images == 0:
            return None
        return self.image_paths[self.current_index]

    def get_label_path(self, image_path):
        return os.path.splitext(image_path)[0] + '.txt'

    def load_image_and_label(self):
        image_path = self.get_current_image()
        if not image_path:
            return None, ""
        label_path = self.get_label_path(image_path)
        label = ""
        if os.path.exists(label_path):
            with open(label_path, 'r', encoding='utf-8') as f:
                label = f.read().strip()
        return Image.open(image_path), label

    def save_label(self, label_text):
        image_path = self.get_current_image()
        if image_path:
            label_path = self.get_label_path(image_path)
            with open(label_path, 'w', encoding='utf-8') as f:
                if image_path not in label_text:
                    f.write(f'{image_path}, "{label_text}"\n')
                else:
                    f.write(label_text)

    def next_image(self, label_text):
        self.save_label(label_text)
        if self.current_index < self.total_images - 1:
            self.current_index += 1
        return self.load_image_and_label(), self.progress()

    def prev_image(self, label_text):
        self.save_label(label_text)
        if self.current_index > 0:
            self.current_index -= 1
        return self.load_image_and_label(), self.progress()

    def progress(self):
        return f"{self.current_index + 1}/{self.total_images}"

# Gradio Interface
def create_gradio_app(folder_path):
    labeler = ImageLabeler(folder_path)

    with gr.Blocks() as demo:
        title = gr.Markdown()

        image = gr.Image(type="pil")
        textbox = gr.Textbox(label="Label", placeholder="Enter label for image")
        progress = gr.Label(visible=False)

        with gr.Row():
            prev_button = gr.Button("⬅️ Previous")
            next_button = gr.Button("➡️ Next")

        def update_prev(label_text):
            (img, lbl), prog = labeler.prev_image(label_text)
            return f"### Image {prog}", img, lbl, prog

        def update_next(label_text):
            (img, lbl), prog = labeler.next_image(label_text)
            return f"### Image {prog}", img, lbl, prog

        def load_initial():
            img, lbl = labeler.load_image_and_label()
            prog = labeler.progress()
            return f"### Image {prog}", img, lbl, prog

        prev_button.click(update_prev, inputs=[textbox], outputs=[title, image, textbox, progress])
        next_button.click(update_next, inputs=[textbox], outputs=[title, image, textbox, progress])
        demo.load(fn=load_initial, inputs=[], outputs=[title, image, textbox, progress])

    return demo

# Run
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--input_dir', type=str, required=True, help='Path to image folder')
    args = parser.parse_args()

    app = create_gradio_app(args.input_dir)
    app.launch()

