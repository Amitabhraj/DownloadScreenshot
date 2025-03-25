from datetime import datetime
import os
from django.contrib import messages
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import random
from secretWinbuzz import settings
from secretWinbuzz.settings import BASE_DIR
from winbuzzSS.models import Deposit_Screenshot 
from PIL import Image, ImageDraw, ImageFont
from winbuzzSS.demo_data import *
# Create your views here.

def firstPage(request):
    context = {}
    if request.method == 'POST':
        deposit_type = request.POST.get('deposit_type')
        amount = int(request.POST.get('amount'))
        amount = str(f"{amount:,}")
        bank_name = request.POST.get('bank_name')
        actual_bank_name = retrieve_bank_name[bank_name]
        last_4_digit_account_number = request.POST.get('last_4_digit_account_number')
        upi_id = request.POST.get('upi_id')
        name = request.POST.get('name')

        utr = str(random.randint(10**11, 10**12 - 1))
        trid = "T" + str(random.randint(10**22, 10**23 - 1))
        self_account_number = str(random.randint(1100, 9091))

        #logo & date time
        if len(name.split(" ")) >= 2:
            words = name.strip().split()
            if len(words) == 1:
                return words[0][0].upper()
            logo = words[0][0].upper() + words[-1][0].upper()
        else:
            logo = name.split(" ")[0][0].upper()

        now = datetime.now() #Current date Time
        date_time = now.strftime("%I:%M %p on %d %b %Y")

        if deposit_type == "BANK":
            image_path = str(BASE_DIR) + "/templates/blank_bank_account.jpg"   # Base template image
            logo_image_path = str(BASE_DIR) + f"/media/logo/{bank_name}.png"

            # Open the image
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)

            # Set the font and size
            font_path = str(BASE_DIR) + "/winbuzzSS/Roboto/Roboto-VariableFont_wdth,wght.ttf"  # Replace with your font path
            date_time_font = ImageFont.truetype(font_path, size=26)
            paid_to_font = ImageFont.truetype(font_path, size=33)
            reciever_account_number_font = ImageFont.truetype(font_path, size=29)
            credited_to_bank_font = ImageFont.truetype(font_path, size=30)
            amount_font = ImageFont.truetype(font_path, size=33)
            transaction_id_font = ImageFont.truetype(font_path, size=29)
            self_account_number_font = ImageFont.truetype(font_path, size=33)
            utr_font = ImageFont.truetype(font_path, size=30)


            # Coordinates for placing text (X, Y positions)
            coords = {
                "date_time":(144,56),
                "paid_to": (162, 216),
                "reciever_last_four_digit_account_number":(388,263),
                "credited_to_bank": (162, 305),
                "amount1": (610, 215),
                "amount2":(613,643),
                "logo":(48,215),
                "transaction_id": (51, 525),
                "self_account_last_four_digit":(292,644),
                "utr": (230, 702)
            }

            # Add the data to the image
            draw.text(coords["date_time"], date_time, fill="#F1FFF1", font=date_time_font)
            draw.text(coords["paid_to"], name, fill="#0E0E0E", font=paid_to_font)
            draw.text(coords["reciever_last_four_digit_account_number"], last_4_digit_account_number, fill="#6C6C6C", font=reciever_account_number_font)
            draw.text(coords["credited_to_bank"], actual_bank_name, fill="#767676", font=credited_to_bank_font)
            draw.text(coords["amount1"], amount, fill="#0E0E0E", stroke_width=0.6, font=amount_font)
            draw.text(coords["amount2"], amount, fill="#1B1B1B", font=amount_font)
            draw.text(coords["transaction_id"], trid, fill="#181818", font=transaction_id_font)
            draw.text(coords["self_account_last_four_digit"], self_account_number, fill="#1B1B1B", font=self_account_number_font)
            draw.text(coords["utr"], utr,  stroke_width=0.2, fill="#7A7A7A", font=utr_font)


            # ✅ Replace the logo text with a circular image
            logo = Image.open(logo_image_path)

            # Resize the logo to fit the desired dimensions
            logo_size = (82, 82)  # Set the desired circle size
            logo = logo.resize(logo_size)

            # Create a circular mask
            mask = Image.new("L", logo.size, 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, logo_size[0], logo_size[1]), fill=255)

            # Create a new image with transparency to hold the circular logo
            circular_logo = Image.new("RGBA", logo.size)
            circular_logo.paste(logo, (0, 0), mask)

            # Paste the circular logo onto the base image
            img.paste(circular_logo, coords["logo"], circular_logo)
            

            final_path_file = str(BASE_DIR) + f"\media\screenshot_{utr}_{trid}.jpg"
            img.save(final_path_file)
            
            response = FileResponse(open(final_path_file, 'rb'))
            filename = f'screenshot_{utr}_{trid}.jpg'
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            download_url = f'/download/?filename={filename}'

            context['download_url'] = download_url
            context['utr'] = utr
            return render(request, 'index.html', context)
        
    return render(request, 'index.html')




def download_image(request):
    filename = request.GET.get('filename')

    if filename:
        image_path = str(BASE_DIR) + f"\media\{filename}"
        response = FileResponse(open(image_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
        






# https://mafia777.online/
# https://winningkro.com/


