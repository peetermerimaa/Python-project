import os.path
from dbfread import DBF
from tkinter import * 
from tkinter import ttk


# abifunktsioon; lõigab asju osadeks
def osadeks(sisu,id=' '):
    return sisu.split(id)


# abifunktsioon; kontrollib, kas andmebaasi asukoht on õigesti sisestatud
def kausta_kontroll(*args):
    kaustanimi = 'C:\\1SBW6\\'+user_dir.get()
    if os.path.exists(kaustanimi):
        kontroll=kaustanimi+'\\'+'1SBOPER.DBF'
        if os.path.isfile(kontroll):
            andmebaas = 'C:\\1SBW6\\'+user_dir.get()+'\\1SBOPER.DBF'
            progress_text.set('Идет обработка базы данных...   ')
            calculate(andmebaas)
        else:
            progress_text.set('Ошибка. Там нет базы данных.')
    else:
        progress_text.set('Ошибка. Нет такой директории.')
 
 
# abifunktsioon; kontrollib andmeid TSD palgalehtedes
def andmete_kontroll():    
    archive=[]
    töötasu={}
    puhkus={}
    
    user=os.getlogin()
    kaust = 'C:\\Users\\'+user+'\\Desktop\\'+user_dir.get()
    
    f = open(kaust+"\\data_arvest.txt", encoding="UTF-8")   
    kuu_max=0
    kuu=0
    for rida in f:
        kontroll_osa=osadeks(rida.strip(),'/')
        kuu = int(osadeks(kontroll_osa[3],'-')[1])
        if kuu > kuu_max:
            kuu_max = kuu 
    for i in range(kuu_max+1):
        archive.append([])
    f.close()
    
    f = open(kaust+"\\data_arvest.txt", encoding="UTF-8")
    for rida in f:
        kontroll_osa=osadeks(rida.strip(),'/')
        kuu=int(osadeks(kontroll_osa[3],'-')[1])
        arvestatud=float(kontroll_osa[1])
        nimi=osadeks(kontroll_osa[0],' ')[2]+' '+osadeks(kontroll_osa[0],' ')[3]
        
        if 'Arvestatud' in kontroll_osa[0] or 'Muud tulud' in kontroll_osa[0]:           
            if nimi not in archive[0]:
                archive[0].append(nimi)
                töötasu[nimi]=0
                puhkus[nimi]=28
            töötasu[nimi]=töötasu[nimi]+arvestatud
    f.close()
    
    n=1
    while n <= kuu_max:
        for i in archive[0]:
            archive[n].append(0)
        n+=1
    
    f = open(kaust+"\\data_arvest.txt", encoding="UTF-8")  
    for rida in f:
        kontroll_osa = osadeks(rida.strip(),'/')
        kuu = int(osadeks(kontroll_osa[3],'-')[1])
        arvestatud = float(kontroll_osa[1])
        nimi = osadeks(kontroll_osa[0],' ')[2]+' '+osadeks(kontroll_osa[0],' ')[3]

        if 'Arvestatud' in kontroll_osa[0] or 'Muud tulud' in kontroll_osa[0]:
            archive[kuu][archive[0].index(nimi)] = arvestatud
        elif 'Puhkuse fond' in kontroll_osa[0]:
            puhkus[nimi] = puhkus[nimi] - float(kontroll_osa[2])
    f.close()
    
    # for i in range(12):
    #     print(archive[i+1][archive[0].index('Knyazev Boris')])
    # print(archive[0][8])        

    #***********************************************************        

    f = open(kaust+"\\andmete_kontroll.txt", 'w', encoding="UTF-8")
    ridade_arv=(len(archive[0])//4)
    start=0
    stop=4
    
    if len(archive[0])<4:
        ridade_arv=1
        stop=len(archive[0])
    
    for i in range(len(archive[0])):
        nimi = str(osadeks(archive[0][i],' ')[0])[0]+'. '+str(osadeks(archive[0][i],' ')[1])
        f.write('{:>16}'.format(nimi))
        
        if (i+1)%4==0:
        #*********************************
            f.write('\n')    
        #*********************************
            n=1
            while n <= kuu_max:
                for k in range(start,stop):
                    f.write('{:>16}'.format(str(archive[n][k])))            
                f.write('\n')
                n+=1            
            ridade_arv-=1
            if ridade_arv > 0:
                start+=4
                stop+=4
            else:
                start += 4
                stop += len(archive[0])%4            
        #*********************************
            f.write('{:>16}'.format(' _______________'*4))
            f.write('\n')

    #****** viimane rida ******
    f.write('\n')
    n=1
    while n <= kuu_max:
        for k in range(start,stop):
            f.write('{:>16}'.format(str(archive[n][k])))            
        f.write('\n')
        n+=1        
    
    f.write('\n\n')

    archive[0].sort()
    for i in range(len(archive[0])):
        lause = archive[0][i]+' - '+str(round(töötasu[archive[0][i]],2))+'\n'
        f.write(lause)
    f.close()
        

# abifunktsioon (rekursioon); otsib kirjavigu perekonnanimedes;
def nimede_kontroll(nimekiri):
    kontroll=[]
    # loome tühi jarjend
    if len(nimekiri)==1:
        return []
    # kõik lõpeb, kui nimekiri lõpeb
    else:    
        baashulk = set(nimekiri[0])
        # iga nimi+perekonnanimi jaoks korraldame kontrolli
        for i in range(1,len(nimekiri)):
            proovihulk = set(nimekiri[i])
            sisu_erinevus = baashulk-proovihulk
            # esimene faktor on sisuline erinevus (peaks olema kas 0 või 1)
            pikkuse_erinevus = abs(len(baashulk)-len(proovihulk))
            # teiseks kontrollime pikkuse erinevust (peaks olema kas 0 või 1)
            if len(sisu_erinevus) <= 1 and pikkuse_erinevus <= 1:
                # kui on karta, et leidsime midagi, kontrollime nimede võrdsust osade kaupa
                esimene_nimi = osadeks(nimekiri[0])
                teine_nimi = osadeks(nimekiri[i])
                if esimene_nimi[0] == teine_nimi[0] or esimene_nimi[1] == teine_nimi[1]:
                    kontroll.append((nimekiri[0],nimekiri[i]))
                    # kui vigased nimed on leitud, siis tagastame kaksikud ennikus
        return kontroll + nimede_kontroll(nimekiri[1:]) 

    
# abifunktsioon; lõppinfo arvutused ja salvestamine faili desktopile
def puhkuse_reserv():
    year=user_year.get()
    user=os.getlogin()
    kaust = 'C:\\Users\\'+user+'\\Desktop\\'+user_dir.get()

    arr_id = []
    arr_nimed = {}
    arr_tooalgus = {}
    arr_puhkpaevad = {}
    arr_tootasu = {}
    arr_keskmine = {}
    arr_tasutapuhk = {}
    arr_mittearvest = {}
    arr_paevad = {}
    arr_puhkused = {}
    arr_eelmine = {}
    arr_seeaasta = {}
    arr_puhkuse_reserv = {}

    d = open(kaust+"\\data_nimekiri.txt", encoding="UTF-8")
    # teeme valmis sõnastikud: nimekiri, tööalgused, palgad, tasutapuhkused 
    for line in d:
        id = osadeks(line,'/')[0]
        arr_id.append(id)
        arr_nimed[id] = osadeks(line,'/')[2]
        arr_tooalgus[id] = osadeks(line,'/')[3]
        arr_mittearvest[id] = int(osadeks(line,'/')[5]) + int(osadeks(line,'/')[6])
        arr_tasutapuhk[id] = int(osadeks(line,'/')[5])
        arr_eelmine[id] = 0
        arr_tootasu[id] = 0
        arr_puhkused[id] = 0
        arr_puhkuse_reserv[id] = 0
    d.close()

    a = open(kaust+"\\data_arvest.txt", encoding="UTF-8")
    for line in a:
        check_kuu = int(osadeks((osadeks(line,'/')[3]),'-')[1])
    piir_line = check_kuu-6
    a.close()

    a = open(kaust+"\\data_arvest.txt", encoding="UTF-8")
    # liidame palgad keskmise töötasu välja arvutamiseks 
    for line in a:
        if int(osadeks((osadeks(line,'/')[3]),'-')[1]) > piir_line:
        # kontrollime töötasu arvestamist (teine poolaasta)
            for i in range(len(arr_id)):
                if arr_nimed[arr_id[i]] in line:
                    arr_tootasu[arr_id[i]] += float(osadeks(line,'/')[1])
    a.close()
    
    # ------------------------------------------------------------------------
    # arvutame välja viimase poolaasta kalendritööpäevad
    for i in range(len(arr_id)):
        kuu = int(osadeks(arr_tooalgus[arr_id[i]],'.')[1])
        paev = int(osadeks(arr_tooalgus[arr_id[i]],'.')[0])
        paevade_kogus = 180
        if osadeks(arr_tooalgus[arr_id[i]],'.')[2] == '17' and int(osadeks(arr_tooalgus[arr_id[i]],'.')[1]) > piir_line:
            if kuu == piir_line + 6:
                paevade_kogus -= (152+paev-1)
                if paev == 25:
                    paevade_kogus += 1
                elif paev == 26:
                    paevade_kogus += 2
                elif paev > 26:
                    paevade_kogus += 3
            elif kuu == piir_line + 5:
                paevade_kogus -= (122+paev-1)
            elif kuu == piir_line + 4:
                paevade_kogus -= (91+paev-1)
            elif kuu == piir_line + 3:
                paevade_kogus -= (61+paev-1)
            elif kuu == piir_line + 2:
                paevade_kogus -= (31+paev-1)
                if paev > 20:
                    paevade_kogus += 1
            elif kuu == piir_line + 1:
                paevade_kogus -= (paev-1)   
        # võtame maha kalendripäevad millal töötaja tööd ei teinud
        paevade_kogus -= arr_mittearvest[arr_id[i]]
        arr_paevad[arr_id[i]] = paevade_kogus
    
    # sellel aastal teenitud puhkusepäevad
    d = open(kaust+"\\data_nimekiri.txt", encoding="UTF-8")
    for line in d:
        id = osadeks(line,'/')[0]
        arr_seeaasta[id] = float(osadeks(line,'/')[7])
    d.close()
    # ------------------------------------------------------------------------
    
    p = open(kaust+"\\data_puhkus.txt", encoding="UTF-8")
    # korjame kokku kõik saadud sellel aastal puhkused
    for line in p:    
        for i in range(len(arr_id)):
            if arr_nimed[arr_id[i]] in line:               
                # kalendritööpaevad miinus saadud puhkused teisel poolaastal
                if int(osadeks((osadeks(line,'/')[3]),'-')[1]) > piir_line:
                    arr_puhkused[arr_id[i]] += int(float(osadeks(line,'/')[2]))
    p.close()
    
    for i in range(len(arr_id)):
        arr_paevad[arr_id[i]] -= arr_puhkused[arr_id[i]]
    
    
    # keskmise töötasu väla arvutamine
    for i in range(len(arr_id)):
        arr_keskmine[arr_id[i]] = arr_tootasu[arr_id[i]] / arr_paevad[arr_id[i]]
    m = open(kaust+'\\puhkuse_reserv.txt', 'w', encoding="UTF-8")
    m.write('\n\n\n')
    m.write('   Puhkuse reserv '+year+'.a.')
    m.write('\n\n\n')
    m.write('{:>68}'.format('0.8%'))
    m.write('{:>9}'.format('33%'))
    m.write('\n')
    sum_puhkusetasu=0
    sum_kindlustus=0
    sum_sotsiaal=0
    for i in range(len(arr_id)):        
        tulemus=arr_seeaasta[arr_id[i]]
        puhkusetasu=arr_keskmine[arr_id[i]]*tulemus
        kindlustus=puhkusetasu/100*0.8
        sotsiaal=puhkusetasu/100*33
        sum_puhkusetasu+=puhkusetasu
        sum_kindlustus+=kindlustus
        sum_sotsiaal+=sotsiaal
        m.write('{:>2}'.format(str(i+1)))
        m.write(' ')
        m.write('{:<25}'.format(arr_nimed[arr_id[i]]))
        m.write('{:>8}'.format(arr_tooalgus[arr_id[i]]))
        m.write('{:>6.1f}'.format(tulemus))
        m.write('{:>8.2f}'.format(arr_keskmine[arr_id[i]]))
        m.write('{:>10.2f}'.format(puhkusetasu))
        m.write('{:>8.2f}'.format(kindlustus))
        m.write('{:>9.2f}'.format(sotsiaal))
        m.write('\n')
    m.write('{:>60.2f}'.format(sum_puhkusetasu))
    m.write('{:>8.2f}'.format(sum_kindlustus))
    m.write('{:>9.2f}'.format(sum_sotsiaal))
    m.close()


# arvutused andmebaasiga; põhilise info läbitöötamine
def calculate(path):
    year=user_year.get()
    user=os.getlogin()
    kaust = 'C:\\Users\\'+user+'\\Desktop\\'+user_dir.get()
    if not os.path.exists(kaust):
        os.makedirs(kaust)
    table = DBF(path, encoding="ISO 8859-5")
    # avame andmebaasifail dbf kus asuvad palgad
    progressi_samm = len(table)//100
    
    f = open(kaust+"\\data_arvest.txt", "w", encoding="UTF-8")
    h = open(kaust+"\\data_hleht.txt", "w", encoding="UTF-8")  
    p = open(kaust+"\\data_puhkus.txt", "w", encoding="UTF-8")
    # avame faili, kuhu kirjutame vajaliku infot, mida leidsime andmebaasist
    progressi_protsent = 0
    # Progressbar konfigureerimine nulliks
    tsd_nimekiri=[]
    haigusleht_nimekiri=[]
    haiguslehed_arvestatud = 0
    # jarjend nimede kokku korjamiseks
    
    for i, record in enumerate(table):

        if i % progressi_samm == 0:
            # Progressbaar loeb andmebaasi read ja kasvab 0%-st kuni 100%-ni
            progressi_protsent += 1
            progress_var.set(progressi_protsent)
            root.update_idletasks()
         
        datatest = osadeks(str(record['OPERDATA']),'-')[0]
        # otsime kasutaja poolt määratud aasta andmed
        if datatest == year:                
            if 'TOO' in record['OPERSOD'] and 'TM:' not in record['OPERSOD']:
                # otsime välja info makstud töötasu kohta 
                if 'Arvestatud' in record['OPERSOD'] or 'Muud tulud' in record['OPERSOD']:
                    nimi = osadeks(record['OPERSOD'])[2]+' '+osadeks(record['OPERSOD'])[3]
                    perenimi = osadeks(record['OPERSOD'])[2]
                    # asendame koodid inimeste nimedega                    
                    if nimi not in tsd_nimekiri:
                        tsd_nimekiri.append(nimi)                      
                    lause = record['OPERSOD']+'/'+str(record['OPERSUM'])+'/'+str(record['OPERKOL'])+'/'+str(record['OPERDATA'])
                    # paneme kirja: Nimi, Perekonnanimi, töötasu ja kuupäev
                    f.write(lause + "\n")                    
                elif 'Puhkuse fond' in record['OPERSOD']:
                    # otsime välja info kasutatud puhkuse kohta
                    if osadeks(str(record['SPSKNO1']))[4]!='8':
                        lause = record['OPERSOD']+'/'+str(record['OPERSUM'])+'/'+str(record['OPERKOL'])+'/'+str(record['OPERDATA'])
                        # paneme kirja: Nimi, Perekonnanimi, kasutatud puhkus ja kuupäev
                        p.write(lause + "\n")
                elif 'Haigusleht' in record['OPERSOD'] and int(osadeks(str(record['OPERDATA']),'-')[1])>6:
                    nimi = osadeks(record['OPERSOD'])[2]+' '+osadeks(record['OPERSOD'])[3]
                    lause = record['OPERSOD']+'/'+str(record['OPERSUM'])+'/'+str(record['OPERKOL'])+'/'+str(record['OPERDATA'])
                    h.write(lause + "\n")                    
                    if nimi not in haigusleht_nimekiri:
                        haiguslehed_arvestatud += 1
                        haigusleht_nimekiri.append(nimi)
                        
    h.close()                
    f.close()
    p.close()
         
    # veel oleks vaja teada saada töölepingutega seotud andmeid; tuleb teha kaks käiku
    table = DBF("C:\\1SBW6\\"+user_dir.get()+"\\"+'1SBCONS.DBF', encoding="ISO 8859-5")
    progressi_samm = len(table)//100

    progressi_protsent = 0
    # progressbar konfigureerimine nulliks
    progress_var.set(progressi_protsent)
    root.update_idletasks()

    indeksid = []
    isikukoodid = {}
    # igal töötajal on oma indeks andmebaasis
        
    for i, record in enumerate(table):
    # esimese käiguga otsime töötajaid nende isikukoodide järgi
        if i % progressi_samm == 0:
            # progressbaar loeb andmebaasi read ja kasvab 0%-st kuni 100%-ni
            progressi_protsent += 1
            progress_var.set(progressi_protsent)
            root.update_idletasks()

        if len(record['CONSVAL']) == 11 and record['CONSVAL'][0] in ['3','4']:
            # otsime töötajaid nende isikukoodide järgi
            if osadeks(record['CONSNAME'])[4][0]=='4':
                # juhul, kui me eksisime isikukoodi numbriga, veendume, et tegu on ikka töötaja indeksiga
                indeksid.append(osadeks(record['CONSNAME'])[4])
                isikukoodid[osadeks(record['CONSNAME'])[4]] = record['CONSVAL']

    progressi_protsent = 0
    # progressbar konfigureerimine nulliks
    progress_var.set(progressi_protsent)
    root.update_idletasks()

    eesnimede_valjad=[]
    perenimede_valjad=[]
    tl_alguse_valjad=[]
    tl_lopu_valjad=[]
    haiguslehe_valjad=[]
    tasutapuhkuse_valjad=[]
    puhkuse_valjad=[]
   
    # andmebasi võtmeväljade struktuur: "M, tühikud, indeks, tühikud, 1 või 2"
    if checked.get() == 1:
        eesnimi_koht = '1'
        perenimi_koht = '2' 
    else:
        eesnimi_koht = '2'
        perenimi_koht = '1'
    
    for i in range(len(indeksid)):
        if len(indeksid[i])==2:
            k=22
        elif len(indeksid[i])==3:
            k=21
        elif len(indeksid[i])==4:
            k=20 
        eesnimede_valjad.append('M'+' '*4+indeksid[i]+' '*k+perenimi_koht)
        perenimede_valjad.append('M'+' '*4+indeksid[i]+' '*k+eesnimi_koht)
        tl_alguse_valjad.append('M'+' '*4+indeksid[i]+' '*k+'6')
        tl_lopu_valjad.append('M'+' '*4+indeksid[i]+' '*(k-1)+'10')
        haiguslehe_valjad.append('M'+' '*4+indeksid[i]+' '*(k-1)+'85')
        tasutapuhkuse_valjad.append('M'+' '*4+indeksid[i]+' '*(k-1)+'75')
        puhkuse_valjad.append('M'+' '*4+indeksid[i]+' '*(k-1)+'95')
    
    indekseerimine = {}
    # sõnastik töötajatele, kus võtmeks on töötaja indeks ja väärtuseks on pere- ja eesnimi
    for i in range(len(indeksid)):
        indekseerimine.setdefault(indeksid[i],'None')
        
    toolepingu_algused = {}
    toolepingu_lopud = {}
    haiguslehed_leitud = 0
    haiguslehed = {}
    tasutapuhkused = {}
    puhkused = {}

    for i, record in enumerate(table):
    # teise käiguga otsime töötajate nimed välja
        if i % progressi_samm == 0:
            # Progressbaar loeb andmebaasi read ja kasvab 0%-st kuni 100%-ni
            progressi_protsent += 1
            progress_var.set(progressi_protsent)
            root.update_idletasks()

        if record['CONSNAME'] in perenimede_valjad:
            # täidame sõnastiku perekonnanimedega
            if indekseerimine[osadeks(record['CONSNAME'])[4]] == 'None':
                indekseerimine[osadeks(record['CONSNAME'])[4]] = record['CONSVAL']
            else:
                indekseerimine[osadeks(record['CONSNAME'])[4]] = indekseerimine[osadeks(record['CONSNAME'])[4]] +' '+ record['CONSVAL'] 
        elif record['CONSNAME'] in eesnimede_valjad:
            # lisame eesnimed
            if indekseerimine[osadeks(record['CONSNAME'])[4]] == 'None':
                indekseerimine[osadeks(record['CONSNAME'])[4]] = record['CONSVAL']
            else:
                indekseerimine[osadeks(record['CONSNAME'])[4]] = record['CONSVAL'] +' '+ indekseerimine[osadeks(record['CONSNAME'])[4]] 
        elif record['CONSNAME'] in tl_alguse_valjad:
            # lisame töölepingu algus
            toolepingu_algused[osadeks(record['CONSNAME'])[4]] = record['CONSVAL']
        elif record['CONSNAME'] in tl_lopu_valjad:
            # lisame töölepingu lõpp
            toolepingu_lopud[osadeks(record['CONSNAME'])[4]] = record['CONSVAL']
        elif record['CONSNAME'] in tasutapuhkuse_valjad:
            # lisame tasutapuhkus
            tasutapuhkused[osadeks(record['CONSNAME'])[4]] = record['CONSVAL']
        elif record['CONSNAME'] in haiguslehe_valjad:
            # lisame haiguslehed
            haiguslehed[osadeks(record['CONSNAME'])[4]] = record['CONSVAL']
            haiguslehed_leitud += 1
        elif record['CONSNAME'] in puhkuse_valjad:
            # lisame puhkused
            puhkused[osadeks(record['CONSNAME'])[4]] = record['CONSVAL']
    
    
    korras = True
    # eeldame et andmebaasis vigu ei ole
    n = open(kaust+"\\data_nimekiri.txt", "w", encoding="UTF-8")
    # avame faili töötajate andmete salvestamiseks    
    if len(indeksid)==0:
        error_text_2.set('Пустая база данных 1С. Работников не найдено.')
        korras = False
    # lisaks kontrollime võimalikud vead töötajate andmebaasis; kui esineb vigu, siis 'korras' muutuja asendatakse 'False' asendisse
    else:
        if  haiguslehed_arvestatud > 0:
            hg = True
            str_nimed = ''
            for i in range(len(haigusleht_nimekiri)):
                str_nimed = str_nimed + str(haigusleht_nimekiri[i])
                if i < len(haigusleht_nimekiri)-1:
                    str_nimed += ', '
                if i == 3 or i == 7 or i == 11 or i == 15:
                    str_nimed += '\n'    
            error_text_3.set('--> Проверьте больничные листы и количество больничных дней:\n' + str_nimed)
            # haiguslehete nimede kontroll
            #    haigusleht_nimekiri.remove(indekseerimine[key])
            #for i in range(len(haigusleht_nimekiri)):
            #    lisa3 = lisa3 + haigusleht_nimekiri[i]+'; '            
        else:
            hg = False
  
        vallandatud = []
        # kõike vallandatud inimesi paigaldame ühte nimekirja
        for i in range(len(indeksid)):
            if indeksid[i] in toolepingu_lopud:
                vallandatud.append(indeksid[i])         
        # eemaldame üldnimekirjast vallandatud isikuid
        for i in range(len(vallandatud)):
            indeksid.remove(vallandatud[i])
  
        for i in range(len(indeksid)):
            lause = indeksid[i]+'/'+isikukoodid[indeksid[i]]+'/'
            # kontrollime, kui andmeid ei ole, siis paneme kirja 'None'
            if indeksid[i] in indekseerimine:
                # Perekonnanimi ja nimi
                lause = lause + indekseerimine[indeksid[i]]+'/'
                lisa1 = ''
            else:
                lause = lause + 'None/'
                korras = False
                lisa1 = '--> Проверьте имена и фамилии работников.\n'
            if indeksid[i] in toolepingu_algused:
                # töölepingu alguse kuupäev
                lause = lause + toolepingu_algused[indeksid[i]]+'/'
                lisa2 = ''
            else:
                lause = lause + 'None/'
                korras = False
                lisa2 = '--> Проверьте даты начала трудовых договоров.\n'
            if indeksid[i] in toolepingu_lopud:
                # töölepingu lõpu kuupäev
                lause = lause + toolepingu_lopud[indeksid[i]]+'/'
            else:
                lause = lause + 'None/'
            if indeksid[i] in tasutapuhkused:
                # tasuta puhkuses viibinud päevade arv
                lause = lause + tasutapuhkused[indeksid[i]]+'/'
            else:
                lause = lause + '0/'
            if indeksid[i] in haiguslehed:
                # haguslehel viibinud päevade arv
                lause = lause + haiguslehed[indeksid[i]]+'/'
            else:
                lause = lause + '0/'
            if indeksid[i] in puhkused:
                # puhkuste päevade arv
                lause = lause + puhkused[indeksid[i]]
            else:
                lause = lause + '0'
            n.write(lause + "\n")
        if korras == False:    
            error_text_1.set('Неполная информация по работникам в базе данных.\n'+lisa1+lisa2)    
    n.close()

   
    # andmebaasi läbivaatamise lõpp
    andmete_kontroll()
    progress_text.set('База данных обработана.')

    print_kirjavead = False
    if len(indeksid)>0:
        kirjavead = nimede_kontroll(tsd_nimekiri)
    else:
        kirjavead = []
        error_text_1.set('Пустая база данных. Проверьте название директории.')
    # kontrollimiseks on töötasu saanud inimeste nimekiri
    
    if len(kirjavead)>0:
        nimede_paarid = ''
        print_kirjavead = True
        # jariendist, kus on eksklikud nimed asuvad ennikutes paaridena, teeme suure sõnumi
        for i in range(len(kirjavead)):
            nimede_paarid = nimede_paarid +'--> '+ str(kirjavead[i]) +'\n'
        error_text_2.set('NB! Подозрение на повторение в ТОО фамилий с опечатками:\n' + nimede_paarid)
    
    if korras == False:  
        info_text.set('К сожалению, расчет резерва отпусков невозможен.\n\nОбнаружены следующие ошибки:')
    elif korras == True:
        info_text.set('Поздравляем!')
        error_text_1.set('Ошибок в базе данных не обнаружено.\nМожно попробовать рассчитать резерв отпусков.')    
    
    show_dataframe2(korras,print_kirjavead,hg)
    # nüüd ilmutame datafame2 ekraanile
    

def show_dataframe2(korras,print_kirjavead,hg):
    # dataframe2 ilmutame ekraanile
    dataframe2 = ttk.Labelframe(mainframe, text=' 2. Расчет резерва отпусков ', padding='5 5 5 5')
    dataframe2.grid(column=0, row=1, columnspan=2, sticky=(W, N, E, S))     
    # dataframe2 - tekstid 5,6,7,8 ja muu stuff    
    text_5=ttk.Label(dataframe2, textvariable=info_text)
    text_5.grid(column=0, row=0, columnspan=2, sticky=(N,W))
    if korras == False:
        arrow1=ttk.Label(dataframe2, image=arrowimg)
        arrow1.grid(column=0, row=1, sticky=(N,E))
    text_6=ttk.Label(dataframe2, textvariable=error_text_1)
    text_6.grid(column=1, columnspan=2, row=1, sticky=(N,W))    
    if korras:
        printpic = ttk.Label(dataframe2, image=printimg)
        printpic.grid(column=0, row=1, rowspan=2, sticky=(W, E, S))
        nupp2 = ttk.Button(dataframe2, text="Рассчитать отпуска", command=puhkuse_reserv)
        nupp2.grid(column=1, row=2, sticky=W)
        ttk.Label(dataframe2, text=' ').grid(column=0, row=4)
    if hg:
        arrow1=ttk.Label(dataframe2, image=arrowimg)
        arrow1.grid(column=0, row=4, sticky=(N,E))
        text_8=ttk.Label(dataframe2, textvariable=error_text_3)
        text_8.grid(column=1, columnspan=2, row=4, sticky=(N,W))            
    if print_kirjavead:
        arrow2=ttk.Label(dataframe2, image=arrowimg)
        arrow2.grid(column=0, row=5, sticky=(N,E))
        text_7 = ttk.Label(dataframe2, textvariable=error_text_2)
        text_7.grid(column=1, row=5, sticky=(N,W))
    for child in dataframe2.winfo_children(): child.grid_configure(padx=5, pady=5)
    #ttk.Label(dataframe2, text=' ').grid(column=2, row=3, padx=30)
    
    
# TKINTER programmi algus
root = Tk()
root.title("Vacation Accounting Pro  /Version 1.0/")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# paneme valmis mõned muutujad
user_dir = StringVar()
user_dir.set('NEWFIRMA')
user_year = StringVar()
user_year.set('2017')
progress_text = StringVar()
progress_var = DoubleVar()
info_text = StringVar()
error_text_1 = StringVar()
error_text_2 = StringVar()
error_text_3 = StringVar()
my_padding='5 5 5 5'
checked=IntVar()
logoimg = PhotoImage(file='img.png')
printimg = PhotoImage(file='print.png')
arrowimg = PhotoImage(file='arrow2.png')

# mainframe // et raam oleks ilus, dataframe1, logoframe
mainframe = ttk.Frame(root, padding='20 20 20 20', relief='ridge',height=800)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

dataframe1 = ttk.Labelframe(mainframe, text=' 1. Обработка базы данных ', padding=my_padding)
dataframe1.grid(column=0, row=0, sticky=(N, W, E))

logoframe = ttk.Frame(mainframe, padding=my_padding)
logoframe.grid(column=1, row=0, sticky=(N, W, E, S))
ttk.Label(logoframe, image=logoimg).grid(column=0, row=0, sticky=(N, W, E, S))

# dataframe1 - tekstid 1,2,3,4 ja muu stuff
text_1 = ttk.Label(dataframe1, text="Введите название директории, где находится база данных 1C: ")
text_1.grid(column=0, row=1, sticky=W, columnspan=3)

s1 = ttk.Separator(dataframe1, orient=HORIZONTAL)
s1.grid(column=0, row=2, sticky=(W, E), columnspan=3)

text_2 = ttk.Label(dataframe1, text="C:\\1SBW6\\ ")
text_2.grid(column=0, row=3, sticky=W)

check = ttk.Checkbutton(dataframe1, text='Имя/Фамилия', variable=checked)
check.grid(column=0, row=6, sticky=(N,W))

dir_entry = ttk.Entry(dataframe1, textvariable=user_dir)
dir_entry.grid(column=1, row=3, sticky=W)
dir_entry.focus()

ttk.Label(dataframe1, text="За отчетный год: ").grid(column=0, row=0, sticky=W)
year_entry = ttk.Entry(dataframe1, width=4, textvariable=user_year)
year_entry.grid(column=1, row=0, sticky=W)

p = ttk.Progressbar(dataframe1, orient=HORIZONTAL, variable=progress_var, length=50, mode='determinate', maximum=100)
p.grid(column=2, row=3, sticky=(E,W))

s2 = ttk.Separator(dataframe1, orient=HORIZONTAL)
s2.grid(column=0, row=4, sticky=(E,W), columnspan=3)

text_3=ttk.Label(dataframe1, textvariable=progress_text)
text_3.grid(column=0, row=5, sticky=W, columnspan=2)

nupp1 = ttk.Button(dataframe1, text="OK", command=kausta_kontroll)
nupp1.grid(column=2, row=5, sticky=E)

# veel natuke joondumist
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
for child in dataframe1.winfo_children(): child.grid_configure(padx=5, pady=5)

root.bind('<Return>', kausta_kontroll)

root.mainloop()
