import tkinter as tk
import boto3
import os
import sys
from tempfile import gettempdir
from contextlib import closing

root= tk.Tk()
root.geometry("800x480")
root.title("Text to speech Converter Amazon Polly")
textExample= tk.Text(root, height=20)
textExample.pack()
def getText():
    aws_mag_con=boto3.session.Session(profile_name='demo_user')
    polly_client=aws_mag_con.client(service_name='polly', region_name='us-east-1')
    result= textExample.get("1.0", tk.END)
    print(result)
    response= polly_client.synthesize_speech(Text=result,OutputFormat='mp3',VoiceId='Matthew')
    print(response)
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output= os.path.join(gettempdir(), "speech.mp3")
            try:
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                print("I/O error")
                sys.exit(-1)
    else:
        print("Could not stream audio")
        sys.exit(-1)
    if sys.platform=="win32":
        os.startfile(output)
btnRead= tk.Button(root,height=1,width=10, text="Read", command=getText)
btnRead.pack()

root.mainloop()

