#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import *
from modeles import modeleResanet
from technique import datesResanet
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask( __name__ )
app.secret_key = 'resanet'


@app.route( '/' , methods = [ 'GET' ] ) # LA ROUTE PAR DEFAUT
def index() :
	return render_template( 'vueAccueil.html' )

@app.route( '/usager/session/choisir' , methods = [ 'GET' ] )
def choisirSessionUsager() :
	return render_template( 'vueConnexionUsager.html' , carteBloquee = False , echecConnexion = False , saisieIncomplete = False )

@app.route( '/usager/seConnecter' , methods = [ 'POST', 'GET' ] )
def seConnecterUsager() :
	if request.method == "POST":
		numeroCarte = request.form[ 'numeroCarte' ] # ICI ON RECUP LE NUMERO DE LA CARTE
		mdp = request.form[ 'mdp' ] # ICI ON RECUP LE MOT DE PASSE

		if numeroCarte != '' and mdp != '' :
			usager = modeleResanet.seConnecterUsager( numeroCarte , mdp ) # On appelle la fonction dans le fichier modeleResanet
			if len(usager) != 0 :
				if usager[ 'activee' ] == True :
					session[ 'numeroCarte' ] = usager[ 'numeroCarte' ] # 1
					session[ 'nom' ] = usager[ 'nom' ]
					session[ 'prenom' ] = usager[ 'prenom' ]
					session[ 'mdp' ] = mdp
					#session['dateCourante'] = datesResanet.getDateAujourdhuiFR()
					session['dateFormatLineaire'] = datesResanet.getDateCourante()
					return redirect( '/usager/reservations/lister' )
					
				else :
					return render_template('vueConnexionUsager.html', carteBloquee = True , echecConnexion = False , saisieIncomplete = False )
			else :
				return render_template('vueConnexionUsager.html', carteBloquee = False , echecConnexion = True , saisieIncomplete = False )
		else :
			return render_template('vueConnexionUsager.html', carteBloquee = False , echecConnexion = False , saisieIncomplete = True)
	else:
		return render_template('404.html')	

@app.route( '/usager/seDeconnecter' , methods = [ 'GET' ] )
def seDeconnecterUsager() :
	# session.pop( 'numeroCarte' , None )
	# session.pop( 'nom' , None )
	# session.pop( 'prenom' , None )
	session = None
	
	return redirect( '/' )
	
@app.route( '/gestionnaire/seDeconnecter' , methods = [ 'GET' ] )
def seDeconnecterGestionnaire() :
	# session.pop( 'login' , None )
	# session.pop( 'nom' , None )
	# session.pop( 'prenom' , None )
	session = None
	print("=> "+str(session))
	return redirect( '/' )


@app.route( '/usager/reservations/lister' , methods = [ 'GET' ] )
def listerReservations() :
	tarifRepas = modeleResanet.getTarifRepas( session[ 'numeroCarte' ] ) # ICI ON RECUP LES TARIFS POUR USER AUTH 
	
	soldeCarte = modeleResanet.getSolde( session[ 'numeroCarte' ] ) # ON RECUP LE SOLDE DE LA CARTE DE USER AUTH
	
	solde = '%.2f' % ( soldeCarte , ) # ON PREND DEUX CHIFFRES APRES LA VIRGULE...

	aujourdhui = datesResanet.getDateAujourdhuiISO() # RECUPERER LA DATE D'AUJOURD'HUI
	
	joursDeLaSemaine = datesResanet.getNomJoursDeLaSemaine()

	datesPeriodeISO = datesResanet.getDatesPeriodeCouranteISO()
	
	datesResas = modeleResanet.getReservationsCarte( session[ 'numeroCarte' ] , datesPeriodeISO[ 0 ] , datesPeriodeISO[ -1 ] )
	
	dates = []
	for uneDateISO in datesPeriodeISO :
		uneDate = {}
		uneDate[ 'iso' ] = uneDateISO
		uneDate[ 'fr' ] = datesResanet.convertirDateISOversFR( uneDateISO )
		
		if uneDateISO <= aujourdhui :
			uneDate[ 'verrouillee' ] = True
		else :
			uneDate[ 'verrouillee' ] = False

		if uneDateISO in datesResas :
			uneDate[ 'reservee' ] = True
		else :
			uneDate[ 'reservee' ] = False
			
		if soldeCarte < tarifRepas and uneDate[ 'reservee' ] == False :
			uneDate[ 'verrouillee' ] = True
			
			
		dates.append( uneDate )
	
	if soldeCarte < tarifRepas :
		soldeInsuffisant = True
	else :
		soldeInsuffisant = False
		
	
	return render_template( 'vueListeReservations.html' , laSession = session , leSolde = solde , lesDates = dates , soldeInsuffisant = soldeInsuffisant, lesJours = joursDeLaSemaine)

	
@app.route( '/usager/reservations/annuler/<dateISO>' , methods = [ 'GET' ] )
def annulerReservation( dateISO ) :
	modeleResanet.annulerReservation( session[ 'numeroCarte' ] , dateISO )
	modeleResanet.crediterSolde( session[ 'numeroCarte' ] )
	return redirect( '/usager/reservations/lister' )
	
@app.route( '/usager/reservations/enregistrer/<dateISO>' , methods = [ 'GET' ] )
def enregistrerReservation( dateISO ) :
	modeleResanet.enregistrerReservation( session[ 'numeroCarte' ] , dateISO )
	modeleResanet.debiterSolde( session[ 'numeroCarte' ] )
	return redirect( '/usager/reservations/lister' )

@app.route( '/usager/mdp/modification/choisir' , methods = [ 'GET' ] )
def choisirModifierMdpUsager() :
	soldeCarte = modeleResanet.getSolde( session[ 'numeroCarte' ] )
	solde = '%.2f' % ( soldeCarte , )
	
	return render_template( 'vueModificationMdp.html' , laSession = session , leSolde = solde , modifMdp = '' )

@app.route( '/usager/mdp/modification/appliquer' , methods = [ 'POST' ] )
def modifierMdpUsager() :
	ancienMdp = request.form[ 'ancienMDP' ]
	nouveauMdp = request.form[ 'nouveauMDP' ]
	
	soldeCarte = modeleResanet.getSolde( session[ 'numeroCarte' ] )
	solde = '%.2f' % ( soldeCarte , )
	
	if ancienMdp != session[ 'mdp' ] or nouveauMdp == '' :
		return render_template( 'vueModificationMdp.html' , laSession = session , leSolde = solde , modifMdp = 'Nok' )
		
	else :
		modeleResanet.modifierMdpUsager( session[ 'numeroCarte' ] , nouveauMdp )
		session[ 'mdp' ] = nouveauMdp
		return render_template( 'vueModificationMdp.html' , laSession = session , leSolde = solde , modifMdp = 'Ok' )


@app.route( '/gestionnaire/session/choisir' , methods = [ 'GET' ] ) #mission 5 : recuperation de la route (connexionGestionnaire)
def choisirSessionGestionnaire() :
	return render_template('vueConnexionGestionnaire.html') #mission 5 : renvoi la page de connexion gestionnaire
	
@app.route('/gestionnaire/seConnecter', methods = [ 'POST'])#mission 5 :cette route est appelée dans la vue vueCOnnexionGestionnaire dans le form
def seConnecterGestionnaire():
	
	login = request.form[ 'login' ] # ICI ON RECUP LE login
	mdp = request.form[ 'mdp' ] # ICI ON RECUP LE MOT DE PASSE 
	
	if login != '' or mdp != '' :
		# ICI LE GESTIONNAIRE A SAISIE DES VALEURS...
		gestionnaire = modeleResanet.seConnecterGestionnaire( login , mdp ) # TENTER D IDENTIFIER L USER VIA LE MODEL (fonction seConnecterUsager)
		if len(gestionnaire) != 0:

				session[ 'login' ] = gestionnaire[ 'login' ] # session est une variable global de type dictionnaire
				session[ 'nom' ] = gestionnaire[ 'nom' ]
				session[ 'prenom' ] = gestionnaire[ 'prenom' ]
			
				return redirect( '/gestionnaire/listerMembresAvecCarte' )
		else:

			return render_template('vueConnexionGestionnaire.html', echecConnexion = True)
	else:

		return render_template('vueConnexionGestionnaire.html',saisieIncomplete = True)

# -------- Membres avec carte ------------

@app.route( '/gestionnaire/listerMembresAvecCarte' , methods = [ 'GET' ] )
def listeMembresAvecCarte():
	personnelsAvecCarte = modeleResanet.getPersonnelsAvecCarte()
	enTeteDuTableauAvecCarte = ['Numero Carte', 'Etat Carte', 'Solde', 'Matricule', 'Nom', 'Prenom', 'Service']
	return render_template('vuePersonnelsAvecCarte.html', listePersonnelsAvecCarte = personnelsAvecCarte, enTeteDuTableau = enTeteDuTableauAvecCarte)

# -------- Membres sans carte ------------

@app.route( '/gestionnaire/listerMembresSansCarte' , methods = [ 'GET' ] )
def listeMembresSansCarte():
	personnelsSansCarte = modeleResanet.getPersonnelsSansCarte()
	enTeteDuTableauPersonnelsSansCarte = ['Matricule','Nom', 'Prenom', 'Service'] #attention si on rajoute un accent il faut rajouter 
	
	return render_template('vuePersonnelsSansCarte.html', listePersonnelsSansCarte = personnelsSansCarte, enTeteDuTableau = enTeteDuTableauPersonnelsSansCarte )

# -------- Crediter ------------

@app.route('/gestionnaire/listerMembresAvecCarte/listerCrediterCarte/crediterCarte' , methods = [ 'POST'])
def membreACrediter():
	numCartePersonnel = request.form[ 'numCartePersonnel' ]
	session['numeroCarte'] = numCartePersonnel
	enTeteDuTableauAvecCarte = ['Numero Carte', 'Etat Carte', 'Solde', 'Matricule', 'Nom', 'Prenom', 'Service']
	return redirect('/gestionnaire/listerMembresAvecCarte/listerCrediterCarte')

@app.route('/gestionnaire/listerMembresAvecCarte/listerCrediterCarte' , methods = [ 'GET'])
def membresAvecCarte():
	enTeteDuTableauAvecCarte = ['Numero Carte', 'Etat Carte', 'Solde', 'Matricule', 'Nom', 'Prenom', 'Service']
	numerodeCarte = session[ 'numeroCarte' ]
	nomMembre = [ 4 ]
	return render_template('vueOperationCrediter.html', enTeteDuTableau = enTeteDuTableauAvecCarte, numeroCarte = numerodeCarte, nomMembre = nomMembre )
	
@app.route('/gestionnaire/listerMembresAvecCarte/listerCrediterCarte/crediterCarte/crediter' , methods = ['POST'])
def crediterCarte():
	numeroCarte = session[ 'numeroCarte' ]
	somme = request.form[ 'somme' ]
	modeleResanet.crediterCarte( numeroCarte , somme )
	
	return redirect('/gestionnaire/listerMembresAvecCarte/listerCrediterCarte')	
	
# -------- Activer et Bloquer ------------
	
@app.route('/gestionnaire/BloquerCarte', methods = ['POST'])
def bloquerMembresAvecCarte():
	numeroDeLaCarte = request.form[ 'numeroCarteBloquer' ]
	modeleResanet.bloquerCarte( numeroDeLaCarte )
	return redirect('/gestionnaire/listerMembresAvecCarte')

@app.route('/gestionnaire/listerMembresAvecCarte/activerCarte', methods = ['POST'])
def activerCarteMembre():
	numeroDeLaCarte = request.form[ 'numeroCarteActiver' ]
	modeleResanet.activerCarte( numeroDeLaCarte )
	return redirect('/gestionnaire/listerMembresAvecCarte')

# -------- Renitialiser mdp ------------

@app.route('/gestionnaire/ActiverCarte', methods = ['POST'])
def activerMembresAvecCarte():
	numeroDeLaCarte = request.form[ 'numeroCarteActiver' ]
	modeleResanet.activerCarte( numeroDeLaCarte )
	return redirect('/gestionnaire/listerMembresAvecCarte')

@app.route('/gestionnaire/ReinitMDP', methods = ['POST'])
def reinitialiserMdp():
	numeroDeLaCarte = request.form[ 'numeroCarte' ]
	modeleResanet.reinitialiserMdp( numeroDeLaCarte )
	return redirect('/gestionnaire/listerMembresAvecCarte')
	
# -------- Historique ------------

@app.route('/gestionnaire/listerMembresAvecCarte/historique', methods = ['POST'])
def historiqueMembre():
	numeroDeLaCarte = request.form[ 'numeroCarte' ]
	historique = modeleResanet.getHistoriqueReservationsCarte( numeroDeLaCarte )
	historique.reverse()
	nbAnnees = []
	nbMois = []
	nbJours = []
	for uneReserv in historique :
		( annee , mois , jour ) = uneReserv.split( '-' )
		nbAnnees.append(annee)
		nbMois.append(mois)
		nbJours.append(jour)
	longueurListe = len(nbJours)
	return render_template('vueHistoriqueCarte.html', numeroCarte = numeroDeLaCarte, Annees = nbAnnees , Mois = nbMois ,Jours = nbJours , longList = longueurListe)

# -------- Creer compte ------------

@app.route('/gestionnaire/listerMembresSansCarte/creationCompte', methods = ['POST'])
def creationCompteRestauration():
	matriculeDuCompte = request.form[ 'matricule' ]
	return render_template('vueCreationCompteRestauration.html', matricule = matriculeDuCompte)

@app.route('/gestionnaire/listerMembresSansCarte/creationCompte/creer', methods = ['POST'])
def creerCompte():
	matriculeDuCompte = session[ 'matricule' ]
	etatDeLaCarte = request.form['etatCarte']
	modeleResanet.creerCarte( matriculeDuCompte , etatDeLaCarte)
	return render_template('vueCreationCompteRestauration.html')

if __name__ == '__main__' :

	app.run( debug = True , host = '127.0.0.1' , port = 5000 )
