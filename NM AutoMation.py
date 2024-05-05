from time import time
st1 = time()
import subprocess

def exce(e):
    file_name=f"logs{f'{e}'[-1]}.txt"
    file=open(file_name,'w')
    file.write(f'{e}')
    file.close()
    print(f"Program Failed/nPlease Contact Developer/nGMAIL: connectwithsanthosh@gmail.com\nUPLOAD {file_name} In Current Program Directory For Better Analysis")
    input("Press Enter To Exit...")
    exit()
def install_library(library_name):
        try:
            print(f"Seems like You Did have {library_name}. So Installing...")
            subprocess.check_call(['pip', 'install', library_name])
            print(f"Successfully installed {library_name}")
        except Exception as e:
            exce(e)            
try:
    from playwright.sync_api import sync_playwright
except:
    install_library("playwright")
subprocess.check_call(['playwright','install'])

    
import json
with open('links.json', 'r') as file:
    data = json.load(file)
try:
    print("MAKE SURE YOUR GIVING CORRECT USER NAME")
    userid=input("User ID: ")
    password=input("Password: ")
    playwright = sync_playwright()
    with playwright as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        def login():
            page.goto("https://hcltech-lms.career-shaper.com/login/index.php")
            page.locator("//input[@id='email']").fill(userid)
            page.locator("//input[@id='password']").fill(password)
            checks = page.query_selector_all('//span[@class="checkmark"]')
            checks[0].click()
            checks[1].click()
            page.get_by_role("button", name="Login").click()
            if page.locator('//div[@class="alert alert-danger"]').is_visible():
                print("Check Username or password and please try agCheck Your User Name Or Passwordain".title())
                exit()
    
        login()
        termi=0
        for i in range(len(data)):
            page.goto(data[i])
            if page.locator("//input[@id='email']").is_visible():
                login()
                page.goto(data[i])
            elif page.locator('//div[@class="message-box"]').is_visible() or page.locator('//video').is_visible():
                continue
            else:
                i=i-1
                termi+=1
                if termi>3:
                    print("something went wrong maybe because of your internet".title())
                    break
                
            data.pop(i)

    browser.close()



    print(f"Execution time: {time() - st1:.2f} seconds")

except Exception as e:
    exce(e)
finally:
   
    if len(data)!=0:
        json_data=json.dumps(data)
        with open('links.json', 'w') as file:
            file.write(json_data)
    else:
        import os
        os.remove("links.json")
    print("make sure you dont have any json fine in this program directory if yes please run this prgram again".title())
