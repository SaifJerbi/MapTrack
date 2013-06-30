

# Create your views here.
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from geo.forms import RegistrationForm, LoginForm
from geo.models import *
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.db import connection

def index(request):
        if request.user.is_authenticated():
                zoom_point=str(request.session.get('zoom_point'))
                zoom=str(request.session.get('zoom'))
                id_provider=str(request.session.get('id_provider'))
                id_societe=str(request.session.get('id_societe'))
                id_connexion=str(request.session.get('id_connexion'))
#                 id_provider = request.GET.get('idp', None).encode('utf8')
#                 id_connexion = request.GET.get('idc', None).encode('utf8')
#                 id_societe = request.GET.get('ids', None).encode('utf8')
                
                query_get_data_from_specific_view = 'SELECT * FROM v_'+id_provider+'_'+id_societe+'_'+id_connexion+' a1,'
                query_get_data_from_specific_view +=' (SELECT voiture, max(dateheure) AS last_date FROM v_1_2_7 GROUP BY v_1_2_7.voiture) a2 '
                query_get_data_from_specific_view +='WHERE a1.voiture = a2.voiture '
                query_get_data_from_specific_view +='AND a1.dateheure = a2.last_date'
                 
                
                waypoints = Waypoint.objects.raw(query_get_data_from_specific_view)
                return render(request, "login.html",{
                    'waypoints': waypoints,
                    'zoom_point':zoom_point[1:-1],
                    'zoom':zoom,
                    })
                ''' user is not submitting the form, show the login form '''
        else:     
                return HttpResponseRedirect('/login/')


def UserProRegistration(request):
        if request.user.is_authenticated():
                return HttpResponseRedirect('/profile/')
        if request.method == 'POST':
                form = RegistrationForm(request.POST)
                if form.is_valid():
                        user = User.objects.create_user(username=form.cleaned_data['username'], email = form.cleaned_data['email'], password = form.cleaned_data['password'])
                        user.save()
                        userPro = UserPro(user=user, telephone=form.cleaned_data['telephone'], adress=form.cleaned_data['adress'])
                        userPro.save()
                        return HttpResponseRedirect('/profile/')
                else:
                        return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
        else:
                ''' user is not submitting the form, show them a blank registration form '''
                return HttpResponseRedirect('/login/')

def LoginRequest(request):
        if request.user.is_authenticated():
            
                return HttpResponseRedirect('/index/')
        if request.method == 'POST':
                form = LoginForm(request.POST)
                if form.is_valid():
                        societe  = form.cleaned_data['societe']
                        #username = form.cleaned_data['username']
                        username = form.cleaned_data.get('username')
                        password = form.cleaned_data['password']
                        usr = username.encode('utf8')
                        pwd = password.encode('utf8')
                        societe = societe.encode('utf8')
                        
                        
                        cursor = connection.cursor()
                        #get Id provider from domain name
                        id_provider=1
                        #    id_provider init to 1 but 
                        #    Require fetching table provide by domain name to get id_provider
                        
                        if id_provider is not None:
                            #get Id societe
                            cursor.execute("SELECT id,id_pays FROM societe WHERE LOWER(raison_sociale) = LOWER(%s) AND id_provider = %s",[societe,id_provider])
                            id_societe = cursor.fetchone()
                            if id_societe is not None:
                                #get Id connexion
                                cursor.execute("SELECT id_user FROM connexion WHERE nom_user = %s AND pwd_user = %s AND id_societe=%s ",[usr,pwd,id_societe[0]])
                                id_connexion = cursor.fetchone()
                                
                                if id_connexion is not None:                                    
                                    #get or create view
                                    query_create_view ="create VIEW v_%s_%s_%s AS select A1.idarchive id, A1.position positio, A1.dop dop, A1.alltitude alltitude, A1.etat etat, A1.dateheure  dateheure, A1.vitesse  vitesse, A2.matricule  voiture, A1.chauffeur  chauffeur, A1.cap cap, A1.disponible  disponible,A1.geo_pos geo_pos, A1.id_archive_local  id_archive_local, A1.inputs inputs, A1.outputs outputs, A1.angle angle, A1.temperature  temperature, A1.etat_porte etat_porte,  A1.niveau_carburant  niveau_carburant, A1.id_delegation  id_delegation,A1.id_ville id_ville, A1.id_localite  id_localite, A1.batterie  batterie,A1.alimentation  alimentation, A1.gps_valid gps_valid, A1.donnee donnee,A1.adresse_source adresse_source  FROM archive A1 , mobile A2 where A1.voiture in(SELECT id_mobile FROM ass_conn_mobile WHERE id_user in (SELECT id_user FROM connexion WHERE nom_user = %s AND pwd_user = %s))AND A1.voiture = A2.id_mobile "
                                    cursor.execute("select * from information_schema.views where table_name='v_%s_%s_%s'",[id_provider,id_societe[0],id_connexion[0]])
                                    #check if View does'nt exist --> create view v_idprovider_idsociete_iduser
                                    if(bool(cursor.rowcount)==False) :
                                        cursor.execute(query_create_view,[id_provider,id_societe[0],id_connexion[0],usr,pwd])    
                                    userPro = authenticate(username=username, password=password)
                                    if userPro is not None:
                                         login(request, userPro)
                                         #get zoom_point Societe's Pays 
                                         cursor.execute("SELECT zoom_point, zoom FROM pays WHERE id_pays = %s ",[id_societe[1]])
                                         zoom_point = cursor.fetchone()
                                
                                         request.session['zoom_point'] = zoom_point[0]
                                         request.session['zoom'] = zoom_point[1]
                                         request.session['id_connexion'] = id_connexion[0]
                                         request.session['id_societe'] = id_societe[0]
                                         request.session['id_provider']=id_provider
                                         return redirect('/index/')
                                         #return HttpResponseRedirect('/index/?idc=%s&ids=%s&idp=%s'% (id_connexion[0], id_societe[0],id_provider))
                                                        # get id mobile
                                                        #get archive by id_voiture
            #                                             for voiture in id_voiture:
            #                                                 id=voiture[0]
            #                                                 waypoints = Waypoint.ojects.raw('''SELECT idarchive AS id, voiture AS name, geo_pos AS geometry FROM archive WHERE voiture = %s ''',[id] )
#                                          waypoints = Waypoint.objects.raw('''SELECT * FROM v_%s_%s_%s Limit 100 ''',[id_provider,id_societe[0],id_connexion[0]])
#                                          for waypoint in waypoints:
#                                              x= waypoint.geo_pos.x
#                                          return render(request, "login.html",{'waypoints': waypoints,})    
                                                        
                                                        #return HttpResponseRedirect('/index/')
                                    else:
                                         return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
                                else :
                                    return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
                                #return msg "username & password failed
                            #return msg "societe does'nt existe        
                        #return msg "provider does'nt exist in data base    
                else:
                        return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
        else:
                ''' user is not submitting the form, show the login form '''
                form = LoginForm()
                context = {'form': form}
                return render_to_response('login.html', context, context_instance=RequestContext(request))

def LogoutRequest(request):
        logout(request)
        return HttpResponseRedirect('/login/')
    
    