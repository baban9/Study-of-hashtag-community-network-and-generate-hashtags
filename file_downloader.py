from instaloader import Instaloader, Hashtag

class downloader:
    def __init__(self, ID, PASS):
        self.loader = Instaloader(
                                    download_pictures=False, 
                                    save_metadata=False, 
                                    download_videos=False, 
                                    quiet=True, 
                                    download_comments=False 
                                )
        self.loader.login(ID, PASS)

    def get_files(self, hashtag_value, folder_loc="text_files", n=50):
        hashtag_vals = Hashtag.from_name(self.loader.context, hashtag_value)
        for i,x in enumerate(hashtag_vals.get_posts()):
            self.loader.download_post(x, folder_loc)
            
            if i == n:
                break
        return True