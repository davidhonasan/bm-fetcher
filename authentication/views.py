from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from bs4 import BeautifulSoup as bs
import requests
from json.decoder import JSONDecodeError


# Views
def splash_page(request):
    return render(request, 'splash.html')


class LoginView(TemplateView):
    template_name = 'authentication/login.html'

    def post(self, request):
        try:
            # Get BM login page
            get_bm_login_page = requests.get('https://binusmaya.binus.ac.id/login/')

            # BM login page soup
            login_soup = bs(get_bm_login_page.text, 'lxml')

            # Get loader.js
            loader_js_url = login_soup.find_all('script')[-1]['src']
            get_loader_js = requests.get('https://binusmaya.binus.ac.id/login/' + loader_js_url)

            # Loader.js soup
            loader_soup = bs(get_loader_js.text, 'lxml')

            # Variables for payload
            login_input = login_soup.find_all('input')
            username_key = login_input[0]['name']
            username_val = request.POST['username']
            password_key = login_input[1]['name']
            password_val = request.POST['password']
            serial1_key = loader_soup.find_all('input')[0]['name']
            serial1_val = loader_soup.find_all('input')[0]['value']
            serial2_key = loader_soup.find_all('input')[1]['name']
            serial2_val = loader_soup.find_all('input')[1]['value']

            # Parameters
            cookie = {'PHPSESSID': get_bm_login_page.cookies['PHPSESSID']}
            payload = {username_key: username_val, password_key: password_val, serial1_key: serial1_val,
                       serial2_key: serial2_val}

            # Authenticate
            requests.post('https://binusmaya.binus.ac.id/login/sys_login.php',
                          headers={'Referer': 'https://binusmaya.binus.ac.id/login/'},
                          cookies=cookie, data=payload)

            # Check if there's JSONDecodeError or not
            info = requests.get('https://binusmaya.binus.ac.id/services/ci/index.php/student/init/indexpage',
                         headers={'Referer': 'https://binusmaya.binus.ac.id/newStudent/'},
                         cookies=cookie).json()

            # Get name, major and student id, cookie
            request.session['name'] = info['Student']['Name']
            request.session['major'] = info['Student']['Major']
            request.session['student_id'] = info['StudentID']
            request.session['session_cookie'] = cookie

            # Adding session cookies and redirect to schedule
            return redirect('schedule:schedule')
        # If JSON error maybe there
        except JSONDecodeError:
            messages.error(request, 'Invalid username or password.')
            return redirect('authentication:login')
        except ConnectionError:
            messages.error(request, 'Connection Error. Please try again.')
            return redirect('authentication:login')