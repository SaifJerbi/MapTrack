from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

# Create your models here.
class Waypoint(models.Model):
    
    
    position = models.PointField(srid=4326)
    dop = models.BigIntegerField()
    alltitude = models.BigIntegerField()
    etat = models.TextField()
    dateheure = models.TimeField()
    vitesse = models.DecimalField(max_digits=11, decimal_places=5)
    voiture = models.CharField(max_length=32)
    cap = models.CharField(max_length=32)
    disponible = models.BooleanField()
    geo_pos = models.PointField(srid=4326)
    id_archive_local = models.BigIntegerField()
    inputs = models.IntegerField()
    outputs = models.IntegerField()
    angle = models.SmallIntegerField()
    temperature = models.DecimalField(max_digits=11, decimal_places=5)
    etat_porte = models.BooleanField()
    niveau_carburant = models.DecimalField(max_digits=11, decimal_places=5)
    id_delegation = models.SmallIntegerField()
    id_ville = models.SmallIntegerField()
    id_localite = models.SmallIntegerField()
    batterie = models.DecimalField(max_digits=11, decimal_places=5)
    alimentation = models.DecimalField(max_digits=11, decimal_places=5)
    gps_valid = models.BooleanField()
    donne = models.TextField()
    adresse_source = models.TextField()
         
    objects = models.GeoManager()

    @classmethod
    def getWayPoint(self):
        waypoints = Waypoint.objects.raw('''SELECT idarchive AS id, voiture AS name, geo_pos AS geometry FROM archive Limit 10 ''' )
        #waypoints = Waypoint.objects.all()
        return waypoints
    
    
    def __unicode__(self):
        return '%s %s' % (self.geo_pos.x, self.geo_pos.y)

class Pays(models.Model):
    
    pays = models.CharField(max_length=500, blank=True)
    zoom_point = models.CharField(max_length=500, blank=True)
    nom_country = models.CharField(max_length=100, blank=True)
    class Meta:
        verbose_name_plural = "Pays"
    
    def __unicode__(self):
        return '%s ' % (self.pays)
#     @classmethod
#     def getImportData(self):
#         pays = Pays.objects.raw('''SELECT id_pays as id, pays as pays, zoom_point as zoom_point, nom_country as nom_country FROM pays ''' )
#         #waypoints = Waypoint.objects.all()
#         
#         for i in pays:
#             s = Pays(i)
#             s.save()
#     
    
class Provider(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    adress = models.CharField(max_length=250)
    
    def __unicode__(self):
        return '%s %s %s' % (self.id,self.name, self.adress)
    
    
class Societe(models.Model):
    id = models.AutoField(primary_key=True)
    raison_sociale = models.CharField(max_length=150, null = True)
    telephone = models.CharField(max_length=150, null = True)
    adresse = models.CharField(max_length=150, null = True)
    ville = models.CharField(max_length=150, null = True)
    logo = models.CharField(max_length=150, null = True)
    website = models.CharField(max_length=150, null = True)
    alerte_payement = models.CharField(max_length=150, null = True)
    frequence_facturation = models.CharField(max_length=150, null = True)
    enabled = models.CharField(max_length=150, null = True)
    fraix_hebergement = models.CharField(max_length=150, null = True)
    mail = models.CharField(max_length=150, null = True)
    sms = models.CharField(max_length=150, null = True)
    id_pays = models.SmallIntegerField( null = True)
    id_provider = models.SmallIntegerField(null = True)
    def __unicode__(self):
        return '%s ' % (self.raison_sociale)
    
    @classmethod
    def getImportData(self):
        societes = Societe.objects.raw('''SELECT id as id, raison_sociale as raison_sociale, telephone as telephone, adresse as adresse, ville as ville, logo as logo, website as website, alerte_payement as alerte_payement,  frequence_facturation as frequence_facturation, enabled as enabled, fraix_hebergement as fraix_hebergement,  mail as mail, sms as sms , id_pays as id_pays , id_pays as id_provider  FROM societe ''' )
        #waypoints = Waypoint.objects.all()

        for i in societes:
            
            i.save()

#from geo.models import *
#Societe.getImportData()
    


class Chauffeur(models.Model):
    
    telephone = models.CharField(max_length=20)
    prenom = models.CharField(max_length=250)
    nom = models.CharField(max_length=250)
    enabled = models.BooleanField()
    adresse = models.CharField(max_length=250)
    societe = models.ForeignKey(Societe)
    dateaffect = models.DateTimeField()
    
    def __unicode__(self):
        return '%s %s -- %s' % (self.prenom, self.nom, self.societe.name)
    
    
 
class Ville(models.Model):
    nom_ville = models.CharField(max_length=100)
    
    def __unicode__(self):
        return '%s ' % (self.nom_ville)
    

class Localite(models.Model):
    nom_localite = models.CharField(max_length=100)
    
    def __unicode__(self):
        return '%s ' % (self.nom_localite)
    
    


    
    
    
class TypeTerminal(models.Model):
    nom_type = models.CharField(max_length=80, blank=True)
    analogic = models.SmallIntegerField(null=True, blank=True)
    can_bus = models.SmallIntegerField(null=True, blank=True)
    
    def __unicode__(self):
        return '%s ' % (self.nom_type)
    
    
class Terminal(models.Model):
    
    num_Terminal = models.CharField(max_length=80, blank=True)
    type_Terminal = models.ForeignKey(TypeTerminal)
    inputs = models.SmallIntegerField(null=True, blank=True)
    outputs = models.SmallIntegerField(null=True, blank=True)
    imei = models.CharField(max_length=80, unique=True)
    
    def __unicode__(self):
        return '%s -- %s ' % (self.num_Terminal, self.type_Terminal.nom_type)
    


class Mobile(models.Model):
    
    nom = models.CharField(max_length=32)
    numtel = models.CharField(max_length=32)
    enabled = models.BooleanField()
    kilometarge = models.DecimalField(max_digits=11, decimal_places=5)
    consommation = models.DecimalField(max_digits=11, decimal_places=5)
    image = models.CharField(max_length=32)
    use_contact = models.BooleanField()
    last_id = models.IntegerField()
    m_login = models.CharField(max_length=32)
    m_password = models.CharField(max_length=32)
    last_id_archive = models.IntegerField()
    matricule = models.CharField(max_length=32)
    matricule_m = models.IntegerField(unique=True)
    societe = models.ForeignKey(Societe)
    distance_vidange = models.SmallIntegerField(default=3000)
    non_supprime = models.BooleanField(default=True)
    has_frontiere_problem = models.BooleanField()
    emplacement = models.CharField(max_length=32)
    connecte = models.BooleanField(default=False)    
    icone_vehicule = models.SmallIntegerField(default=12)
    v_max_carburant = models.DecimalField(max_digits=11, decimal_places=5)
    capacite_carburant = models.DecimalField(max_digits=11, decimal_places=5)
    v_min_carburant = models.DecimalField(max_digits=11, decimal_places=5)
    survitesse = models.IntegerField(default=110)
    terminal = models.ForeignKey(Terminal)
    
    def __unicode__(self):
        return '%s -- %s ' % (self.nom, self.numtel)
    
from django.contrib.auth.models import User

class Connexion(models.Model):
    nomuser = models.CharField(max_length=50,null=True)
    pwduser = models.CharField(max_length=50,null=True)
    id_societe = models.IntegerField(null=True)
    enabled = models.BooleanField()
    roleuser = models.SmallIntegerField(default = 0)
    repindex = models.BigIntegerField(null=True)
    @classmethod
    def getImportData(self):
        connexions = Connexion.objects.raw('''SELECT id_user as id, nom_user as nom_user, pwd_user as pwd_user,id_societe as id_societe,enabled as enabled,role_user as role_user, rep_index as rep_index FROM connexion ''' )
        #waypoints = Waypoint.objects.all()

        for i in connexions:           
            i.save()
            
#from geo.models import *
#Connexion.getImportData()   
class UserPro(models.Model):
    
    user = models.OneToOneField(User,primary_key=True)
    adress = models.CharField(max_length=250)
    telephone = models.CharField(max_length=250)
    societe = models.ForeignKey(Societe)
    mobiles = models.ManyToManyField(Mobile)
    class Meta:
        unique_together = (("user", "societe"),)
    
    @classmethod
    def getUserLoged(self, username, pwd):
        user = UserPro.objects.filter(login=username, password=pwd )
        return user
    @classmethod
    def getImportData(self):
        u = UserPro.objects.raw('''SELECT id_user as user_id, nom_user as adress, pwd_user as telephone FROM connexion ''' )
        #from geo.models import *
        #UserPro.getImportData() 
        
        for i in u:  
            usrname = i.adress
            pwd = i.telephone
            x = User.objects.create_user(usrname,'',pwd)         
            
    
    def __unicode__(self):
        return '%s %s -- %s' % (self.user.first_name, self.user.last_name, self.societe.raison_sociale)
   
    
class Archive(models.Model):
    position = models.PointField(srid=4326)
    dop = models.BigIntegerField(default=0)
    alltitude = models.BigIntegerField(default=0)
    etat = models.TextField(default='0')
    dateheure = models.DateTimeField()
    vitesse = models.DecimalField(max_digits=11, decimal_places=5)
    mobile = models.ForeignKey(Mobile)
    chauffeur = models.ForeignKey(Chauffeur)
    cap = models.CharField(max_length=32)
    disponible = models.BooleanField()
    geo_pos = models.PointField(srid=4326)
    inputs = models.CharField(max_length=32)
    outputs = models.CharField(max_length=32)
    angle = models.SmallIntegerField()
    temperature = models.DecimalField(max_digits=11, decimal_places=5)
    etat_porte = models.BooleanField()
    niveau_carburant = models.DecimalField(max_digits=11, decimal_places=5)
    pays = models.ForeignKey(Pays)
    ville = models.ForeignKey(Ville)
    localite = models.ForeignKey(Localite)
    batterie = models.DecimalField(max_digits=11, decimal_places=5)
    alimentation = models.DecimalField(max_digits=11, decimal_places=5)
    gps_valid = models.BooleanField(default=True)
    donne = models.TextField(default='Vide')
    adresse_source = models.TextField(default='0.0.0.0')
    
    @classmethod
    def getArchive(self):
        archives = Archive.objects.raw('''SELECT idarchive AS id, position AS position FROM archive Limit 10 ''' )
        return archives
    
    def __unicode__(self):
        #return '%s -- %s, %s, %s ' % (self.mobile.nom, self.localite.name, self.ville.name, self.pays.name)
        return '%s ' % (self.position)
    

   
class Traduction (models.Model):  
    francais = models.CharField(max_length=32)
    arabe = models.CharField(max_length=32)
    anglais = models.CharField(max_length=32)
    
    def __unicode__(self):
        return '%s ' % (self.francais)
    
    
class Language(models.Model):
    name = models.CharField(max_length=32)
    pays = models.ForeignKey(Pays)
    abreviation = models.CharField(max_length=5)
    def __unicode__(self):
        return '%s - %s ' % (self.name, self.pays.name)
    
class Menu(models.Model):
    valeur = models.CharField(max_length=32)
    language = models.ForeignKey(Language) 
    def __unicode__(self):
        return '%s - %s' % (self.valeur, self.language.abreviation)
class AccessRules(models.Model):
    name = models.CharField(max_length=60)
           
    def __unicode__(self):
        return '%s ' % (self.name)
    
    
class Permission(models.Model):
    name = models.CharField(max_length=60)
    accessRules = models.ManyToManyField(AccessRules)
   
    def __unicode__(self):
        return '%s ' % (self.name)
    
    

    
    
    
    
    
    
    
    

    
    

 