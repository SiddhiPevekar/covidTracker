# from django.contrib.auth import authenticate
from . import models
# Create your views here.
from django.shortcuts import redirect, render
import requests
from .models import Booking, Oxygen, Patient, Supplier
from matplotlib import pyplot as plt
from django.contrib import messages
from django.db.models import F

user_s =""
user_p =""
book_s =""

def download_data() -> dict:
#     """
#         Downloads currently available data from scraped from 
#         'https://www.mohfw.gov.in/' website.
#     """
    r = requests.get('https://covid19-mohfw.herokuapp.com/', auth=('user', 'pass'))

    if(r.status_code == 200):
        print('Request Successful!')
    else:
        print('Request Failed!')

    data = r.json()
    return data

# Create your views here.
def homepage(request):
    data_dict = download_data()
    country_data = data_dict['totals']
    state_data = data_dict['states']

    d = { 
            'active_cases' : country_data["cases"] , 
            'recovered' : country_data["recoveries"], 
            'deaths' : country_data["deaths"], 
            'state_list' : state_data                 # List of states(table-rows)
        }
    create_image(state_data)
    
    return render(request, 'information/index.html' , d)
    
    # return render(request, 'information/index.html')

def create_image(state_data):
    data = []
    # print(state_list)
    for state in state_data:
        cur = [ state['cases'] ,state['recoveries'] ,state['deaths'] , state['state'] ]

        data.append(cur)

    data.sort(reverse = True)
    data = data[:10]

    print(len(data))

    y = [d[0] for d in data]
    x = [d[-1] for d in data]

    # print(x, y)
    plt.figure(figsize=(15, 5))
    print(x)
    plt.bar(x,y,color='#2222AF')
    plt.xlabel('States')
    plt.ylabel('Active Cases')

    # plt.show()
    # pprint(data)
    plt.savefig('information/static/information/assets/img/s1.png')

# if __name__ == '__main__':
#     data_dict = download_data()
#     country_data = data_dict['totals']
#     state_list = data_dict['states']
#     create_image(state_list)

def supplier_register(request):
   if request.method == "POST":
        s_agency_name = request.POST.get('s_agency_name')
        s_emailid = request.POST.get('s_emailid')
        s_govcode=request.POST.get('s_govcode')
        s_pass1 = request.POST.get('s_pass1')
        s_pass2 = request.POST.get('s_pass2')
        oxygen = request.POST.get('oxygen')
        if s_pass1!=s_pass2:
            messages.success(request, 'Your Re-entered Password does not match to Password')
        else:
            supplier_record = models.Supplier(s_agency_name=s_agency_name, s_emailid=s_emailid, s_pass1=s_pass1, s_pass2=s_pass2,s_govcode=s_govcode)
            supplier_record.save()
            oxy_record= models.Oxygen(oxygen=oxygen)
            oxy_record.save()
            print("Data has been saved")
        return redirect('/')

def s_loginpage(request):
    # global user_s
    if request.method == "POST":
        username = request.POST.get('s_emailid', False)
        password= request.POST.get('s_password', False)
        print(username)
        print(password)
        # user_s = username
        # print(user_s)
        bool_ans = models.Supplier.objects.filter(s_emailid=username, s_password=password).exists()#condition to match values are equal or not
        # request.session['supplier']=username
        if bool_ans == True:
            request.session['supplier']=username
            # name=request.session['supplier']
            # print(name)
            # sup= models.Supplier.objects.filter(s_emailid = username)
            # supval = {
            #     "supplier": sup #to get particular object
            # # }  
            # return render(request, 'information/supplier_home.html',supval)   
            sup= Supplier.objects.filter(s_emailid = request.session["supplier"])   
            print(sup)   
            return render(request, 'information/supplier_home.html', {'supplier':sup, 'supplier_data': request.session["supplier"]})
        if bool_ans == False:
            # return render(request, 'information/index.html')
            return redirect('/')

    return render(request, 'information/supplier_home.html')#where the form is present

def patient_register(request):
   if request.method == "POST":
        p_username = request.POST.get('p_username')
        p_firstname = request.POST.get('p_firstname')
        p_lastname = request.POST.get('p_lastname')
        p_emailid = request.POST.get('p_emailid')
        p_pass1 = request.POST.get('p_pass1')
        p_pass2 = request.POST.get('p_pass2')
        if p_pass1!=p_pass2:
            messages.success(request, 'Your Re-entered Password does not match to Password')
        else:
            patient_record = models.Patient(p_username=p_username, p_firstname=p_firstname, p_lastname=p_lastname, p_emailid=p_emailid, p_pass1=p_pass1, p_pass2=p_pass2)
            patient_record.save()
            print("Data has been saved")
        return redirect('/')
#    return render(request, 'information/index.html')



def patient_login(request):
    # global user_p
    # data = Supplier.objects.all()
    # print(data)
    if request.method == "POST":
        p_username = request.POST.get('p_username', False)
        p_pass1= request.POST.get('p_pass1', False)
        # print(p_username)
        # user_p = p_username
        # print(user_p)
        bool_ans = models.Patient.objects.filter(p_username=p_username, p_pass1=p_pass1).exists()
        if bool_ans == True:
            request.session['patient']=p_username
            pat= models.Patient.objects.filter(p_username= request.session["patient"])
            # patval = {
            #     "patient": pat,
            #     # "supplier_info": data
            # }
            messages.success(request, 'Successfully loggedin')
            return render(request, 'information/patient_homepage.html',{'patient':pat, 'patient_data': request.session["patient"]})
        if bool_ans == False:
            return redirect('/')
            # return render(request, 'information/index.html')
    return render(request, 'information/patient_homepage.html')

def logout_user(request):
    # global user_s
    # global user_p
    # user_s =""
    # user_p =""
    del request.session['supplier']
    return redirect('/')

def profile_patient(request):
    global user_p
    if user_p!="":
        print(user_p)
        pat = models.Patient.objects.filter(p_username=user_p)
        patval = {
            "patient": pat
        }

        return render(request, 'information/patient_profile.html',patval)
    return render(request, 'information/patient_profile.html')
    
def update_patient(request):
    global user_p
    data = Supplier.objects.all()
    if user_p!="":
        print(user_p)
        pat = models.Patient.objects.filter(p_username=user_p)
        if request.method == 'POST':
            # s_id = request.POST.get('s_id')
            p_username = request.POST.get('p_username')
            p_firstname = request.POST.get('p_firstname')
            p_lastname = request.POST.get('p_lastname')
            p_emailid = request.POST.get('p_emailid')
            p_pass1 = request.POST.get('p_pass1')
            p_pass2 = request.POST.get('p_pass2')
            for i in pat:
                i.p_username = p_username
                i.save()
                i.p_firstname = p_firstname
                i.save()
                i.p_lastname = p_lastname
                i.save()
                i.p_emailid = p_emailid
                i.save()
                i.p_pass1 = p_pass1
                i.save()
                i.p_pass2 = p_pass2
                i.save()
            print("Details saved")
            patient = {
                "pat_d": pat,
                "supplier_info": data
            }

        return render(request,'information/patient_homepage.html', patient)

    return render(request, 'information/patient_homepage.html')

def update_supplier(request):
    # global user_s 
    # if user_s!="":
    #     print(user_s)
    if request.session.has_key('supplier'):
        #supp is kind array of object
        # supp = models.Supplier.objects.filter(s_emailid=user_s)
        supp = models.Supplier.objects.filter(s_emailid=request.session["supplier"])
        if request.method == 'POST':
            # s_id = request.POST.get('s_id')
            s_agency_name = request.POST.get('s_agency_name')
            s_state = request.POST.get('s_state')
            s_emailid = request.POST.get('s_emailid')
            s_password = request.POST.get('s_password')
            s_district = request.POST.get('s_district')
            icu_beds = request.POST.get('icu_beds')
            ventilator_beds= request.POST.get('ventilator_beds')
            icu_ventilator_beds = request.POST.get('icu_ventilator_beds')
            oxygen = request.POST.get('oxygen')
            for i in supp:
                i.s_agency_name = s_agency_name
                i.save()
                i.s_state = s_state
                i.save()
                i.s_emailid = s_emailid
                i.save()
                i.s_password = s_password
                i.save()
                i.s_district = s_district
                i.save()
                i.icu_beds = icu_beds
                i.save()
                i.ventilator_beds = ventilator_beds
                i.save()
                i.icu_ventilator_beds = icu_ventilator_beds
                i.save()
                i.oxygen = oxygen
                i.save() 
            print("Details saved")
            supplier = {
                "sup": supp
            }
        return render(request, 'information/index.html', supplier)
    return render(request, 'information/index.html')

def book_now(request):
    global user_p
    print(user_p)
    global book_s
    book_s = ""
    patient=Patient.objects.filter(p_username=user_p)
    if request.method == 'POST':
        s_govcode = request.POST.get('s_govcode')
        print(s_govcode)
        gov_id_data=Supplier.objects.filter(s_govcode=s_govcode)
        print(gov_id_data)
        book_s = s_govcode
        print(book_s)
        gov={
            "s_gov_id":gov_id_data,
            "current_patient":patient
        }
        return render(request, 'information/book_requirement.html', gov)
    return render(request, 'information/book_requirement.html')

def book(request):
    global user_p
    global book_s 
    print(user_p)
    print(book_s)
    data = Supplier.objects.all()
    pat= {
        "supplier_info": data
    }
    if user_p!="":
        print(user_p)
        if request.method == "POST":
            bed = request.POST.get('bed', False)
            oxygen = request.POST.get('oxygen', False)
            patient=request.POST.get('patient', False)
            supplier=request.POST.get('supplier', False)
            b_patient=Patient.objects.get(p_username=patient)
            b_supplier=Supplier.objects.get(s_agency_name=supplier)
            Booking.objects.create(
                bed=bed,
                oxygen=oxygen,
                patient=b_patient,
                supplier=b_supplier
            )
            print(supplier)
            if bed=="ICU":
                b_supplier=Supplier.objects.get(s_agency_name=supplier)
                b_supplier.icu_beds=F('icu_beds')-1
                b_supplier.save()
            elif bed=="Ventilator":
                b_v=Supplier.objects.get(s_agency_name=supplier)
                b_v.ventilator_beds=F('ventilator_beds')-1
                b_v.save()
            elif bed=="ICU+Ventilator":
                b_i=Supplier.objects.get(s_agency_name=supplier)
                b_i.icu_ventilator_beds=F('icu_ventilator_beds')-1
                b_i.save()

        return render(request,'information/patient_homepage.html', pat)
    return render(request,'information/patient_homepage.html', pat)

# def health_care(request):
#     return render(request, 'information/health_care.html')