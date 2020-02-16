#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime


def convertirDateISOversFR( dateISO ) :
	annee , mois , jour = dateISO.split( '-' )
	dateFR = '/'.join( ( jour , mois , annee ) )
	return dateFR
	
def convertirDateFRversISO( dateFR ) :
	jour , mois , annee = dateFR.split( '/' )
	dateISO = '-'.join( ( annee , mois , jour ) )
	return dateISO	
	
def getDateAujourdhuiFR() :
	dateCourante = datetime.datetime.today()
	aujourdhui = '%02d/%02d/%04d' % ( dateCourante.day , dateCourante.month , dateCourante.year )
	return aujourdhui
	
def getDateAujourdhuiISO() :
	dateCourante = datetime.datetime.today()
	aujourdhui = '%04d-%02d-%02d' % ( dateCourante.year , dateCourante.month , dateCourante.day )
	return aujourdhui
	
def getDatesPeriodeCouranteISO() :
	dates = []
	
	dateAujourdhui= datetime.datetime.today()
	numJourAujourdhui = dateAujourdhui.weekday()
	
	dateCourante = dateAujourdhui - datetime.timedelta( numJourAujourdhui )
	
	for i in range( 12 ) :
		if i != 5 and i != 6 :
			dateISO = '%04d-%02d-%02d' % ( dateCourante.year , dateCourante.month , dateCourante.day )
			dates.append( dateISO )
			
		dateCourante = dateCourante + datetime.timedelta( 1 )
		 
	return dates
	
def getNomJoursDeLaSemaine():
	nomsDates = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi" ,"Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
	return nomsDates
	
def getDatesPeriodeCouranteFR():
	dates = []

	dateAujourdhui = datetime.datetime.today()
	numJourAujourdhui = dateAujourdhui.weekday()

	dateCourante = dateAujourdhui - datetime.timedelta(numJourAujourdhui)

	for i in range(12):
		if i != 5 and i != 6:
			dateFR = '%02d/%02d/%04d' % (dateCourante.day, dateCourante.month, dateCourante.year)
			dates.append(dateFR)

		dateCourante = dateCourante + datetime.timedelta(1)

	return dates
	
def getDateCourante():
    
    d = datetime.datetime.today()
    jour = d.strftime("%d")
    mois = d.strftime("%B")
    annee = d.strftime("%Y")
    if 'January' in mois:
        return ('%s, %s %s' %(jour, 'Janvier', annee))
    
    if 'February' in mois:
        return ('%s, %s %s' %(jour, 'Février', annee))
    
    if 'March' in mois:
        return ('%s, %s %s' %(jour, 'Mars', annee))
    
    if 'April' in mois:
        return ('%s, %s %s' %(jour, 'Avril', annee))
    
    if 'May' in mois:
        return ('%s, %s %s' % (jour, 'Mai', annee))
    
    if 'June' in mois:
        return ('%s, %s %s' %(jour, 'Juin', annee))
    
    if 'July' in mois:
        return ('%s, %s %s' %(jour, 'Juillet', annee))
    
    if 'August' in mois:
        return ('%s, %s %s' %(jour, 'Aout', annee))
    
    if 'September' in mois:
        return ('%s, %s %s' %(jour, 'Septembre', annee))
    
    if 'October' in mois:
        return ('%s, %s %s' %(jour, 'Octobre', annee))
    
    if 'November' in mois:
        return ('%s, %s %s' %(jour, 'Novembre', annee))
    
    if 'December'in mois:
        return ('%s, %s %s' %(jour, 'Décembre', annee))

if __name__ == '__main__' :
	print(convertirDateUSversFR( '2017-02-01' ))
	print (convertirDateFRversUS( '01/02/2017' ))
	print (getDateAujourdhuiFR())
	print (getDateAujourdhuiUS())
	
	dates = getDatesPeriodeCouranteUS()
	for uneDate in dates :
		print(uneDate)
