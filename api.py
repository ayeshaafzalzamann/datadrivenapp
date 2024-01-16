from tkinter import RIGHT, font, ttk, Button, Frame, Label
from PIL import Image, ImageTk
import io
import requests
import tkinter as tk
from urllib.parse import urlparse
import pycountry


def switch_to_frame(frame):
    frame.tkraise()

def is_image_url(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme in ('http', 'https') and any(parsed_url.path.lower().endswith(ext) for ext in ('.png', '.jpg', '.jpeg', '.gif'))

def load_flag_image(flag_url):
    try:
        response = requests.get(flag_url)
        response.raise_for_status()
        flag_image = Image.open(io.BytesIO(response.content))
        flag_image = flag_image.resize((100, 60), resample=Image.LANCZOS)
        flag_image = ImageTk.PhotoImage(flag_image)
        return flag_image
    except Exception as e:
        print(f"Error loading flag image: {e}")

def fetch_country_data(country_code):
    url = f'https://restcountries.com/v3.1/alpha/{country_code}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def update_display():
    selected_country = country_combobox.get()
    if selected_country:
        country_data = fetch_country_data(selected_country)
        if country_data:
            display_country_info(country_data)
        else:
            result_label.config(text="Error fetching data")
    else:
        result_label.config(text="Please select a country")

def display_country_info(country_data):
    if isinstance(country_data, list) and country_data:
        country_data = country_data[0]

    name = country_data.get('name', {}).get('common', 'N/A')
    capital = country_data.get('capital', ['N/A'])[0]
    population = country_data.get('population', 'N/A')
    flag_url = country_data.get('flags', {}).get('png', None)
    currencies = country_data.get('currencies', ['N/A'])
    languages = country_data.get('languages', ['N/A'])

    result_text = f"Name: {name}\nCapital: {capital}\nPopulation: {population}\n"
    result_text += f"Currencies: {', '.join(currencies)}\n"
    result_text += f"Languages: {', '.join(languages)}"

    result_label.config(text=result_text)

    # Clear the previous flag image
    flag_label.config(image=None)

    if flag_url and is_image_url(flag_url):
        flag_image = load_flag_image(flag_url)
        if flag_image:
            flag_label.config(image=flag_image)
            flag_label.image = flag_image
    else:
        flag_label.config(image=None)

def clear_display():
    # Clear the displayed information and flag image
    result_label.config(text="")
    flag_label.config(image=None)

def get_country_code(country_name):
    try:
        country_code = pycountry.countries.search_fuzzy(country_name)[0].alpha_3
        return country_code
    except LookupError:
        return None

def page2():
    switch_to_frame(frame2)

def page3():
    switch_to_frame(frame3)

def page4():
    switch_to_frame(frame4)

def fetch_all_regions():
    url = 'https://restcountries.com/v3.1/all'
    response = requests.get(url)

    if response.status_code == 200:
        countries = response.json()
        all_regions = set()

        for country in countries:
            if 'region' in country:
                region = country['region']
                if region and isinstance(region, str):
                    all_regions.add(region)

        return list(all_regions)
    else:
        return []



def update_display_by_region():
    selected_region = region_combobox.get()
    if selected_region:
        country_data_by_region = fetch_country_data_by_region(selected_region)
        if country_data_by_region:
            display_country_info_by_region(country_data_by_region)
        else:
            result_by_region_label.config(text="Error fetching data")
    else:
        result_by_region_label.config(text="Please select a region")

def fetch_country_data_by_region(region):
    url = f'https://restcountries.com/v3.1/region/{region.lower()}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def display_country_info_by_region(country_data_by_region):
    if isinstance(country_data_by_region, list) and country_data_by_region:
        country_data_by_region = country_data_by_region[0]

    name_by_region = country_data_by_region.get('name', {}).get('common', 'N/A')
    capital_by_region = country_data_by_region.get('capital', ['N/A'])[0]
    population_by_region = country_data_by_region.get('population', 'N/A')
    flag_url_by_region = country_data_by_region.get('flags', {}).get('png', None)
    currencies_by_region = country_data_by_region.get('currencies', ['N/A'])
    languages_by_region = country_data_by_region.get('languages', ['N/A'])

    result_text_by_region = f"Name: {name_by_region}\nCapital: {capital_by_region}\nPopulation: {population_by_region}\n"
    result_text_by_region += f"Currencies: {', '.join(currencies_by_region)}\n"
    result_text_by_region += f"Languages: {', '.join(languages_by_region)}"

    result_by_region_label.config(text=result_text_by_region)

    # Clear the previous flag image
    flag_by_region_label.config(image=None)

    if flag_url_by_region and is_image_url(flag_url_by_region):
        flag_image_by_region = load_flag_image(flag_url_by_region)
        if flag_image_by_region:
            flag_by_region_label.config(image=flag_image_by_region)
            flag_by_region_label.image = flag_image_by_region
    else:
        flag_by_region_label.config(image=None)

def clear_display_by_region():
    # Clear the displayed information and flag image for region
    result_by_region_label.config(text="")
    flag_by_region_label.config(image=None)

# Fetch all regions dynamically
all_regions = fetch_all_regions()


root = tk.Tk()
root.title("Restcountries API GUI")
root.geometry("400x600")
root.config(bg="#203354")


#now creating frames
frame1=Frame(root,bg="#203354")
imgframe=ImageTk.PhotoImage(Image.open("exploring world.png"))
imglabel= Label(frame1, image=imgframe)
imglabel.place(x=0,y=0, width=400 , height=600)

#creating button and using font

italic_font = font.Font(size=15, slant="italic",weight="bold")
b1 = Button(frame1,text="START", command=page2,font=italic_font,
            bg='white',fg='#934821',border=10)
b1.place(x=120, y=417, width=170,height=50)
frame1.place(x=0 ,y= 0,height=600,width=400)

#now second frame
frame2=Frame(root,bg="#203354")

imgframe2=ImageTk.PhotoImage(Image.open("second vbackground.png"))
imglabel= Label(frame2, image=imgframe2)
imglabel.place(x=0,y=0, width=400 , height=600)
#buttons
b2 = Button(frame2, text="🢦",font=('Arial',25),fg="white", bg="#8B4513",
             command=lambda: switch_to_frame(frame1))
b3 = Button(frame2, text="➪", font=('Arial',19),fg="white", bg="#8B4513", command=page3)
b2.place(x=0, y=0, width=30 , height=30)
b3.place(x=369, y=0 , width=30 , height=30)

#now creating the label
l1=Label(frame2, text="App Information",font=("Instrument Serif",20))
l1.place(x=110,y=40)


#creating another frame for text
l2=Label(frame2,text="Welcome to explore world application.\n This application is based on countries api which \nallow user to access the data of the countries.\nThe user have to select the country code to display \nthe information",font=30)
l2.place(x=20,y=150,height=300,width=365)



frame2.place(x=0 ,y= 0,height=600,width=400)
#frame 3
frame3=Frame(root,bg="#203354")

imgframe3=ImageTk.PhotoImage(Image.open("exploring world (1).png"))
imglabel= Label(frame3, image=imgframe3)
imglabel.place(x=0,y=0, width=400 , height=600)

b4 = Button(frame3, text="🢦",font=('Arial',25),fg="white", bg="#8B4513",
             command=page2)
b4.place(x=0, y=0, width=30 , height=30)

b5 = Button(frame3, text="➡", font=('Arial', 19), fg="white", bg="#8B4513", command=page4)
b5.place(x=369, y=0, width=30, height=30)

label=Label(frame3, text="Select code to get countries",font=("Instrument Serif",12))
label.place(x=110,y=30)


# Country selection
countries = requests.get('https://restcountries.com/v3.1/all').json()
country_names = [country['cca3'] for country in countries]
country_combobox = ttk.Combobox(frame3, values=country_names)
country_combobox.pack(pady=65)

# Buttons
fetch_button = tk.Button(frame3, text="Fetch Country Info", command=update_display)
fetch_button.pack(side=tk.RIGHT, padx=5)

clear_button = tk.Button(frame3, text="Clear", command=lambda: result_label.config(text=""))
clear_button.pack(side=tk.LEFT, padx=5)

# Display Frame
display_frame = Frame(frame3,background="white",)
display_frame.pack(pady=10,padx=20)

# Display result
result_label = tk.Label(frame3, text="",height=10,width=35,background="#fff")
result_label.place(x=70 ,y=150)

# Flag display
flag_label = tk.Label(frame3)
flag_label.pack(pady=150)



frame3.place(x=0 ,y= 0,height=600,width=400)

# Fourth Frame (frame4) modifications
frame4 = Frame(root, bg="#203354")

imgframe4 = ImageTk.PhotoImage(Image.open("exploring world (1).png"))
imglabel = Label(frame4, image=imgframe4)
imglabel.place(x=0, y=0, width=400, height=600)

label=Label(frame4, text="Select regions to get countries",font=("Instrument Serif",12))
label.place(x=110,y=30)

b5 = Button(frame4, text="➡", font=('Arial', 19), fg="white", bg="#8B4513", command=page3)
b5.place(x=369, y=0, width=30, height=30)

# Region selection
region_combobox = ttk.Combobox(frame4, values=all_regions)
region_combobox.pack(pady=65)


# Buttons
fetch_by_region_button = tk.Button(frame4, text="Fetch by Region", command=update_display_by_region)
fetch_by_region_button.pack(side=tk.RIGHT, padx=5)

clear_by_region_button = tk.Button(frame4, text="Clear", command=clear_display_by_region)
clear_by_region_button.pack(side=tk.LEFT, padx=5)

# Display Frame for region
display_by_region_frame = Frame(frame4, background="white")
display_by_region_frame.pack(pady=10, padx=20)

# Display result for region
result_by_region_label = tk.Label(frame4, text="", height=10, width=35, background="#fff")
result_by_region_label.place(x=70, y=150)

# Flag display for region
flag_by_region_label = tk.Label(frame4)
flag_by_region_label.pack(pady=150)



# Fetch all regions dynamically
all_regions = fetch_all_regions()

# Update values in region_combobox
region_combobox['values'] = all_regions





frame4.place(x=0,y=0,height=600,width=400)

#initially switch to frame 1
switch_to_frame(frame1)
root.mainloop()

