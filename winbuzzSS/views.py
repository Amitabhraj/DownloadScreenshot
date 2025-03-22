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
# Create your views here.

def firstPage(request):
    context = {}
    if request.method == 'POST':
        # try:
        deposit_type = request.POST.get('deposit_type')
        amount = int(request.POST.get('amount'))
        amount = str(f"{amount:,}")
        bank_name = request.POST.get('bank_name')
        last_4_digit_account_number = request.POST.get('last_4_digit_account_number')
        upi_id = request.POST.get('upi_id')
        name = request.POST.get('name')
        utr = str(random.randint(10**11, 10**12 - 1))
        trid = "T"+str(random.randint(10**22, 10**23 - 1))
        self_account_number = str(random.randint(1100, 9091))

        # Generating random UTR, TRID, and account number
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
            image_path = str(BASE_DIR) + "/templates/bank_account_blank.jpg"   # Base template image

            # Open the image
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)

            # Set the font and size
            font_path = str(BASE_DIR) + "/winbuzzSS/Roboto/Roboto-VariableFont_wdth,wght.ttf"  # Replace with your font path
            date_time_font = ImageFont.truetype(font_path, size=25)
            paid_to_font = ImageFont.truetype(font_path, size=32)
            reciever_account_number_font = ImageFont.truetype(font_path, size=28)
            credited_to_bank_font = ImageFont.truetype(font_path, size=28)
            amount_font = ImageFont.truetype(font_path, size=33)
            transaction_id_font = ImageFont.truetype(font_path, size=28)
            self_account_number_font = ImageFont.truetype(font_path, size=33)
            utr_font = ImageFont.truetype(font_path, size=28)
            logo_font = ImageFont.truetype(font_path, size=36)


            # Coordinates for placing text (X, Y positions)
            coords = {
                "date_time":(143,58),
                "paid_to": (159, 216),
                "reciever_last_four_digit_account_number":(305,262),
                "credited_to_bank": (160, 304),
                "amount1": (593, 215),
                "amount2":(593,637),
                "logo":(68,230),
                "transaction_id": (49, 520),
                "self_account_last_four_digit":(279,638),
                "utr": (225, 697)
            }

            # Add the data to the image
            draw.text(coords["date_time"], date_time, fill="#dad9d9", stroke_width=0.3, font=date_time_font)
            draw.text(coords["paid_to"], name, fill="#ece9e9", font=paid_to_font)
            draw.text(coords["reciever_last_four_digit_account_number"], last_4_digit_account_number, fill="#b8b5b8", font=reciever_account_number_font)
            draw.text(coords["credited_to_bank"], bank_name, fill="#b8b5b8", font=credited_to_bank_font)
            draw.text(coords["logo"], logo, fill="white", stroke_width=0.2, font=logo_font)
            draw.text(coords["amount1"], amount, fill="#dad9d9", stroke_width=0.3, font=amount_font)
            draw.text(coords["amount2"], amount, fill="#d2d1d1", stroke_width=0.3, font=amount_font)
            draw.text(coords["transaction_id"], trid, fill="#e7e3e7", stroke_width=0.2, font=transaction_id_font)
            draw.text(coords["self_account_last_four_digit"], self_account_number, fill="#e7e3e7", font=self_account_number_font)
            draw.text(coords["utr"], utr, fill="#b8b5b8", font=utr_font)
            
            
            # Save data to the database
            Deposit_Screenshot.objects.create(
                deposit_type=deposit_type,
                amount=amount,
                last_4_digit_account_number=last_4_digit_account_number,
                upi_id=upi_id,
                name=name,
                utr=utr,
                trid=trid,
                bank_name = bank_name,
                self_account_number=self_account_number
            )

            final_path_file = str(BASE_DIR) + f"\media\screenshot_{utr}_{trid}.jpg"
            img.save(final_path_file)
            response = FileResponse(open(final_path_file, 'rb'))

            filename = f'screenshot_{utr}_{trid}.jpg'
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

            print(response)

            # Redirect to the same page after download
            download_url = f'/download/?filename={filename}'

            context['download_url'] = download_url
            context['utr'] = utr
            return render(request, 'index.html',context)
        # except Exception:
        #     messages.success(request,'Some Error Occured, Plzz Try Again')
        #     return render(request, 'index.html')
        
    return render(request, 'index.html')




def download_image(request):
    filename = request.GET.get('filename')

    if filename:
        image_path = str(BASE_DIR) + f"\media\{filename}"
        response = FileResponse(open(image_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
        



