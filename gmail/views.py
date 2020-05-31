from django.shortcuts import render,redirect
from gmail.form import Login,send_form,fetch_mail
from gmail.mail_send import send_smtp
from gmail.rec_mail import receive_pop,num_mail,delete_msg
# Create your views here.

def index(request):
    form=Login()
    if request.method=='POST':
        form=Login(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            request.session['email'] = email
            request.session['password'] = password
            return redirect('home')
    return render(request,'index.html',{'form':form})

def home(request):
     if request.session.get('email'):
        context={
                'email':request.session.get('email'),
                }
        return render(request,'home.html',context)
    else:
        return redirect('index')



def logout(request):
    try:
        del request.session['email']
        del request.session['password']
        del request.session['fetch']
      
    except:
        pass
    return redirect('index')

def send_mail(request):
    if request.session.get('email'):
        from_email=request.session.get('email')
        form=send_form(initial={'From':from_email})
        if request.method=='POST':
            form=send_form(request.POST,request.FILES)
            if form.is_valid():
                to_email=form.cleaned_data['To']
                cc_email=form.cleaned_data['CC']
                bcc_email=form.cleaned_data['BCC']
                subject=form.cleaned_data['subject']
                try:
                    my_file=request.FILES['attach']
                except:
                    my_file=None
                message=form.cleaned_data['message']
                password=request.session.get('password')
                msg_send=send_smtp(from_email,password,to_email,cc_email,bcc_email,subject,my_file,message)
                if msg_send:
                    return render(request,'send.html',{'msg_send':msg_send,'send_form':form})
                else:
                    return redirect('send_mail')

        context={
                'email':request.session.get('email'),
                'send_form':form,
                }
        return render(request,'send.html',context)

    else:
        return redirect('index')    

def receive_mail(request):
    if request.session.get('email'):
        from_email=request.session.get('email')
        password=request.session.get('password')
        try:
            mail_num=num_mail(from_email,password)
            form=fetch_mail(initial={'fetch_num':mail_num})
            if request.method=='POST':
                form=fetch_mail(request.POST)
                if form.is_valid():
                    fetch=form.cleaned_data['fetch']
                    request.session['fetch']=fetch
                    mail_rec=mail_num-int(fetch)+1
                    from_mail,to_mail,cc_mail,subject,body=receive_pop(from_email,password,mail_rec)
                    context={'email':from_email,
                            'fetch_form':form,
                            'from_fetch':from_mail,
                            'to_fetch':to_mail,
                            'cc_fetch':cc_mail,
                            'sub_fetch':subject,
                            'body_fetch':body
                    }
                    return render(request,'receive.html',context)
                else:
                    context={
                        'email':from_email,
                        'fetch_form':form
                    }
                    return render(request,'receive.html',context)
            else:
                request.session['fetch']=mail_num
                if mail_num!=0:
                    from_mail,to_mail,cc_mail,subject,body=receive_pop(from_email,password,mail_num)
                    context={
                        'email':from_email,
                        'fetch_form':form,
                        'from_fetch':from_mail,
                        'to_fetch':to_mail,
                        'cc_fetch':cc_mail,
                        'sub_fetch':subject,
                        'body_fetch':body
                    }
                else:
                    context={
                        'email':from_email,
                        'no_mail':'Inbox Empty',
                        'fetch_form':form,
                    }
                return render(request,'receive.html',context)
        except:
            context={
                'network_msg':'please connect to your internet',
                'email':from_email
            }
            return render(request,'receive.html',context)

    else:
        return redirect('index')

def delete_mail(request):
    if request.session.get('email'):
        email=request.session.get('email')
        password=request.session.get('password')
        fetch=request.session.get('fetch')
        delete_msg(email,password,int(fetch))
        return redirect('receive_mail')
    else:
        return redirect('index')
