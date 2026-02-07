import streamlit as st
from pathlib import Path
import time
import os
from bs4 import BeautifulSoup
import random
import requests
import html


############### Title ###############
st.set_page_config(layout="wide")
st.columns([1])
html_title = """
<style>
    .title-test {
    font-weight:bold; 
    padding:5px; 
    border-radius:6px;
    }
</style>
<center><h1 class="title-test">Album Download Platform</h1></center>
"""
st.markdown(body=html_title, unsafe_allow_html=True)

st.header("Select the HTML files you would like to download")
upload_files = st.file_uploader(label="Choose the html file", type='html', accept_multiple_files=True, 
                               width="stretch")
st.divider()

st.header("Select the local directory where you do save your photos")
figsave_dir = st.text_input(label="Enter Local Directory (Required)", placeholder="CLICK ENTER TO CONFIRM YOUR directory")


if figsave_dir.strip():   # if not typing anything in figsave_dir, .strip() will return False.
    figsave_dir = Path(figsave_dir)
    # st.write("Your assigned directory is valid !!")
    # st.write("It is {}".format(figsave_dir))

    if os.path.isdir(figsave_dir) == False or len(upload_files) == 0:
        if os.path.isdir(figsave_dir) == False:
            st.write("Your directory doesn't exist !!")
        if len(upload_files) == 0:
            st.write("You didn't upload any html file !!")
    
    else:
        st.markdown(
        f"""
        <p style="margin:0 0 -1px 0;">Your assigned directory is valid !! Click 'Start Download' to fetch the photos.</p>
        <p style="margin:0 100px 0 0;">It is {figsave_dir}</p>
        """, unsafe_allow_html=True,
        )
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)   # as a spacer between button and sentences

        if st.button(label="Start Download") and os.path.isdir(figsave_dir):

            user_agent_list=[
                        'Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0)',
                        'Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.0;Trident/4.0)',
                        'Mozilla/4.0(compatible;MSIE7.0;WindowsNT6.0)',
                        'Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11',
                        'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
                        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
                        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',  
                        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
                        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
                    ]

            album_level_status = st.empty()
            album_level_progress = st.progress(0)
            album_level_progress_text = st.empty()
            album_total = len(upload_files)
            album_status_text = st.empty()


            for i, upload_file in enumerate(upload_files):
                soup = BeautifulSoup(upload_file.read().decode("utf-8"), "html.parser")
                pure_html = "\n".join(html.unescape(td.get_text()) for td in soup.select("td.line-content"))
                doc = BeautifulSoup(pure_html, "html.parser")
                img_lst = doc.find_all(attrs={'class':'ui image kit-prevent-select kit-prevent-drag ftea_post_module_image'})

                album_status_text = "Downloading {} album".format(i + 1)
                album_level_progress.progress((i + 1) / album_total)    # show+update the downloaded status
                album_level_progress_text.write(f"Number {i + 1} out of {album_total} photos has been downloaded") 
                status_text = st.empty()  # status text for the current album download
                total = len(img_lst)

                progress = st.progress(0)   # show progress for the current download album
                # start downloading the img images in the album
                for j, img_info in enumerate(img_lst):
                    progress.progress((j + 1) / (total))
                    status_text.write(f"Number {j + 1} out of {total} photos has been processed")
                    try:
                        img_url = img_info.get('data-src')
                        img_name = img_url.split('/')[-1]
                        response_pic = requests.get(img_url, headers = {'user_agent':random.choice(user_agent_list)}).content
                        with open(os.path.join(figsave_dir, img_name + '.jpg'), 'wb') as images:
                            images.write(response_pic)
                        
                    except:
                        st.write("Number {} img failed to be fetched".format(j + 1))

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)   # as a spacer
            time.sleep(1)
            st.success("Full process has been done !")




            # for i in range(album_total):
            #     album_status_text = "Downloading {} album".format(i)
            #     status_text = st.empty()
            #     total = 30
            #     album_level_progress.progress((i + 1) / album_total)   # show+update the downloaded status
            #     album_level_progress_text.write(f"Number {i + 1} out of {album_total} photos has been downloaded") 

            #     progress = st.progress(0)
            #     for j in range(total):
            #         progress.progress((j + 1) / (total))
            #         status_text.write(f"Number {j + 1} out of {total} photos has been downloaded")
            #         time.sleep(0.1)
            # time.sleep(1)
            # st.success("All photos downloaded!")
