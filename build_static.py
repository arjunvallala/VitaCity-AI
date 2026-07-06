"""
VitaCity AI — Static Build Script for Netlify
Aggregates all Python app files and packages them into a single stlite (WebAssembly) HTML bundle.
"""

import os
import json

TEMPLATE = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
    <title>VitaCity AI — Decision Intelligence Platform</title>
    <link rel="icon" href="https://emoji.slack-edge.com/T024F4BC8/city/9df6f4d994.png" type="image/png" />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.58.0/build/stlite.css" />
    <style>
      /* Custom loader styling while WebAssembly loads */
      #stlite-loader {
        position: fixed;
        inset: 0;
        background: #091013;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #F0F6FF;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        z-index: 9999;
      }
      .spinner {
        width: 50px;
        height: 50px;
        border: 3px solid rgba(86, 199, 216, 0.15);
        border-radius: 50%;
        border-top-color: #4CC9F0;
        animation: spin 1s linear infinite;
      }
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
      .title {
        font-size: 24px;
        font-weight: 600;
        margin-top: 24px;
        letter-spacing: -0.02em;
      }
      .subtitle {
        font-size: 14px;
        color: #8B9EC5;
        margin-top: 8px;
        text-align: center;
        max-width: 400px;
        line-height: 1.5;
        padding: 0 20px;
      }
    </style>
  </head>
  <body>
    <div id="stlite-loader">
      <div class="spinner"></div>
      <div class="title">Loading VitaCity AI</div>
      <div class="subtitle">Running Python & Streamlit entirely in your browser via WebAssembly (first load takes 10-15s to download runtimes)...</div>
    </div>
    <div id="root"></div>
    <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.58.0/build/stlite.js"></script>
    <script>
      const files = @FILES_JSON@;
      
      stlite.mount(
        {
          requirements: ["scikit-learn", "pandas", "plotly", "pillow", "python-dotenv"],
          entrypoint: "app.py",
          files: files,
        },
        document.getElementById("root")
      );
      
      // Hide loader once app is mounted and visible
      const observer = new MutationObserver((mutations, obs) => {
        const app = document.querySelector(".stApp");
        if (app) {
          document.getElementById("stlite-loader").style.display = "none";
          obs.disconnect();
        }
      });
      observer.observe(document.getElementById("root"), {
        childList: true,
        subtree: true
      });
    </script>
  </body>
</html>
"""

def main():
    print("Building static stlite app for Netlify...")
    files = {}
    
    # Files to include
    include_dirs = ["core", "data", "ui"]
    include_files = ["app.py"]
    
    for f in include_files:
        if os.path.exists(f):
            with open(f, "r", encoding="utf-8") as fh:
                files[f] = fh.read()
                
    for d in include_dirs:
        if os.path.exists(d):
            for root, _, filenames in os.walk(d):
                for filename in filenames:
                    if filename.endswith(".py"):
                        fp = os.path.join(root, filename)
                        rel_path = os.path.relpath(fp)
                        # Normalize path separators to forward slashes for stlite virtual fs
                        rel_path = rel_path.replace("\\", "/")
                        with open(fp, "r", encoding="utf-8") as fh:
                            files[rel_path] = fh.read()
                            
    os.makedirs("public", exist_ok=True)
    
    # Inject JSON
    files_json = json.dumps(files)
    html_content = TEMPLATE.replace("@FILES_JSON@", files_json)
    
    with open("public/index.html", "w", encoding="utf-8") as fh:
        fh.write(html_content)
        
    print(f"Successfully packaged {len(files)} files into public/index.html")

if __name__ == "__main__":
    main()
