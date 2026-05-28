from PIL import Image, ImageDraw, ImageFont
import os
import shutil

backup_dir = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8"
img_dir = r"c:\Users\jacob\Downloads\TFG\Documento final\Img"

img_bak_name = "conexion_nodo_ambiente_1779985459934.png"
img_bak = os.path.join(backup_dir, img_bak_name)
img_dest = os.path.join(img_dir, "conexion_nodo_ambiente.png")

font_path = r"C:\Windows\Fonts\arial.ttf"

def get_font(size):
    try:
        return ImageFont.truetype(font_path, size)
    except IOError:
        return ImageFont.load_default()

if not os.path.exists(img_bak):
    print("Backup image not found!")
    exit()

# Step 1: Restore the COMPLETE original image - no modifications
shutil.copy(img_bak, img_dest)
print("Step 1: Restored original backup completely")

with Image.open(img_dest) as img:
    draw = ImageDraw.Draw(img)
    bg_color = img.getpixel((930, 640))
    
    # Step 2: Only remove the top header text (as requested before)
    draw.rectangle([0, 0, 1024, 140], fill="white")
    print("Step 2: Removed header text")
    
    # Step 3: Understand the original layout
    # In the original:
    #   - Relay module is at x=785-920, y=672-975
    #   - Screw terminals (NO, COM, NC) are at the TOP (y~672-700)
    #   - Blue casing with "Relay Module" text in the MIDDLE
    #   - Control pins (VCC, IN, GND) are at the BOTTOM (y~955-975)
    #   - Wires go from breadboard (y=614) DOWN to the TOP of the relay (y=672)
    #     connecting to the SCREW TERMINALS - this is WRONG
    #   - Below the relay there's the "1-Channel Relay" text label
    
    # Step 4: Crop the relay module AND the label text below it
    # The relay body is y=672 to y=975, label text below to ~y=1000
    relay_box = (785, 672, 920, 975)
    relay_crop = img.crop(relay_box)
    
    # Step 5: Rotate the relay 180 degrees
    rotated_relay = relay_crop.rotate(180)
    
    # Step 6: Clean up the upside-down text on the rotated relay
    r_draw = ImageDraw.Draw(rotated_relay)
    crop_w, crop_h = rotated_relay.size  # 135 x 303
    
    # After rotation:
    # - The old "1-Channel Relay" label (was below relay) is now at the TOP of the crop (y=0-18ish)
    #   Paint it with canvas bg color so it blends
    r_draw.rectangle([0, 0, crop_w, 20], fill=bg_color)
    
    # - The old VCC/IN/GND pin labels (were at bottom) are now near the TOP (y~18-50)
    #   These are on the green PCB. Paint over with PCB blue color and redraw
    pcb_blue = (42, 134, 201)
    r_draw.rectangle([10, 20, crop_w-10, 50], fill=pcb_blue)
    
    # Draw VCC, IN, GND labels right-side up
    font_pins = get_font(11)
    r_draw.text((22, 28), "VCC", fill="white", font=font_pins)
    r_draw.text((60, 28), "IN", fill="white", font=font_pins)
    r_draw.text((90, 28), "GND", fill="white", font=font_pins)
    
    # - The blue casing text ("Relay Module", "5V", Songle logo) is upside down in the middle
    #   Paint over the casing area with the light blue casing color and redraw
    casing_blue = (130, 196, 244)
    # The casing spans roughly y_crop=70 to y_crop=230 in the rotated crop
    r_draw.rectangle([40, 70, 108, 230], fill=casing_blue)
    
    # Redraw "Relay Module" and "5V DC" right-side up on the casing
    font_casing = get_font(14)
    font_small = get_font(11)
    r_draw.text((52, 110), "Relay", fill="white", font=font_casing)
    r_draw.text((45, 130), "Module", fill="white", font=font_casing)
    r_draw.text((55, 165), "5V DC", fill="white", font=font_small)
    
    # - The old screw terminal labels (NO, COM, NC were at top) are now at the BOTTOM
    #   These should be fine since they face down. But any wire stubs that were
    #   at the top in the original are now dangling at the bottom after rotation.
    #   Paint white over the bottom area below the terminals to remove wire stubs.
    r_draw.rectangle([0, crop_h-18, crop_w, crop_h], fill=(255,255,255))
    
    # Step 7: Paste the cleaned rotated relay back
    img.paste(rotated_relay, (785, 672))
    print("Step 5-7: Rotated relay, cleaned text, pasted back")
    
    # Step 8: Write "1-Channel Relay" right-side up below the relay
    font_label = get_font(13)
    # Clear any old text area below the relay
    draw.rectangle([785, 975, 920, 1000], fill=(255,255,255))
    draw.text((798, 978), "1-Channel Relay", fill="black", font=font_label)
    print("Step 8: Added label below relay")
    
    # The wires that were originally going from the breadboard to the TOP of the relay
    # are STILL THERE and UNCHANGED. But now the TOP of the relay has the control pins
    # (VCC, IN, GND) instead of the screw terminals. So the connections are now CORRECT.
    # No need to redraw any wires!
    
    img.save(img_dest)
    print("DONE. Saved corrected image.")
