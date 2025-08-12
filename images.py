import os
import re
import shutil

# Paths
posts_dir = "/home/vishwa/vblog/content/posts/"
attachments_dir = "/home/vishwa/obsidian_vault/Second_Brain/blog-attachments/"
static_images_dir = "/home/vishwa/vblog/static/images/"

# Step 1: Process each markdown file in the posts directory
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        
        with open(filepath, "r") as file:
            content = file.read()
        
        # Step 2: Find all Obsidian-style image links: ![[image.png]]
        images = re.findall(r'\[\[([^]]*\.png)\]\]', content)
        print(images)
        # Step 3: Replace image links with Hugo relURL shortcode
        for image in images:
            hugo_image = f'![Image Description]({{\"images/{image.replace(" ", "%20")}\" | relURL }})'
            content = content.replace(f'![[{image}]]', hugo_image)
            # Step 4: Copy the image to the Hugo static/images directory if it exists
            image_source = os.path.join(attachments_dir, image)
            if os.path.exists(image_source):
                shutil.copy(image_source, static_images_dir)

        # Step 5: Write the updated content back to the markdown file
        with open(filepath, "w") as file:
            file.write(content)

print("Markdown files processed and images copied successfully.")
