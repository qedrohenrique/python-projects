from PIL import ImageQt
import requests
import PySimpleGUI as sg
from io import BytesIO
from pytube import YouTube

def image_to_data(im):
  """
  Image object to bytes object.
  : Parameters
    im - Image object
  : Return
    bytes object.
  """
  with BytesIO() as output:
    im.save(output, format="PNG")
    data = output.getvalue()
  return data

def create_image_from_url(url):
  '''
  Instantiate an image object from an url and resizes it
  :return sg.Image
  :param str
  '''
  
  response = requests.get(url, stream=True)
  response.raw.decode_content = True
  img = ImageQt.Image.open(response.raw).resize((200,150), ImageQt.Image.ANTIALIAS)
  data = image_to_data(img)
  return data, (200,150)
   
def instantiate_video(url): 
  '''
  Instantiate a YouTube object
  :return YouTube object, string of thumbnail url
  :param str
  '''
  
  video_url = url
  yt = YouTube(video_url)
  thumbnail_url = yt.thumbnail_url
  
  return yt, thumbnail_url

# Creating GUI

img_box = sg.Image(None, key = '-IMG-')

left_column = [[img_box], [sg.Text("", key = '-OUT-', size = (20,30))]]
right_column = [[sg.Text("Make sure to type a valid url")],[sg.InputText(key = '-IN-')], [sg.Button(button_text = "Search"), sg.Button(button_text = "Download")]]

layout = [[sg.Column(left_column, vertical_alignment = 'c', element_justification='c', size = (200,300)), sg.VSeparator(), sg.Column(right_column, element_justification='c')]]

window = sg.Window('Multiple Format Image Viewer', layout, size = (500,300))

# Event calling

while True:
  event, values = window.read()
  
  # Search event
  
  if event == 'Search':
    input_url = values['-IN-']
    yt, thumbnail = instantiate_video(input_url)
    data, size = create_image_from_url(thumbnail)
    window['-IMG-'].update(data = data, size = size)
    window['-OUT-'].update(yt.title)
    window.refresh()
  
  if event == 'Download':
    if yt is None:
      break
    video = yt.streams.get_highest_resolution()
    video.download('Downloads')
  
  # Closing events
  if event is None:
    break
  if event in (sg.WIN_CLOSED, 'Quit'):
    break
window.close()