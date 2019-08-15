use BBR2017
GO
declare @kommunekode int
declare @Max_BYG_ANVEND_KODE int 


set @kommunekode = 741
set @Max_BYG_ANVEND_KODE = 600



declare @kaelderareal table (Bygning_id uniqueidentifier, K�lderareal_under_125cm int)
insert into @kaelderareal (Bygning_id, K�lderareal_under_125cm)
	select 
		Etage.Bygning_id 
		, sum(Etage.KAELDER_ARL_U_125M) as K�lderareal_under_125cm
	from  BBR2017.dbo.CO40500T Etage 
		INNER JOIN BBR2017.dbo.CO40100T Bygning ON Etage.Bygning_id = Bygning.Bygning_id
	where 	
		Etage.ObjStatus = 1
		AND Bygning.KomKode = @kommunekode
		AND	Bygning.BYG_ANVEND_KODE < 600
		AND	Bygning.BYG_ANVEND_KODE > 0
		AND Bygning.BYG_ARL_SAML > 0
		AND Bygning.OPFOERELSE_AAR > 0
		AND Bygning.ObjStatus = 1
	group by Etage.Bygning_id
	

SELECT Bygning.Bygning_id AS Bygningsid
	, Bygning.BYG_ANVEND_KODE AS Bygningsanvendelse
	, Bygning.OPFOERELSE_AAR AS Opf�relses�r
	, Bygning.OMBYG_AAR AS Ombygnings�r
	, Bygning.TAG_KODE AS Tagkode
	, Bygning.SuppTagDaekMat AS SuppTagDaekMat
	, Bygning.YDERVAEG_KODE AS Yderv�gkode
	, Bygning.SuppYderVaegMat AS SuppYderVaegMat
	, Bygning.VARMEINSTAL_KODE AS Varmeinstalationskode
	, Bygning.OPVARMNING_KODE AS Opvarmningskode
	, Bygning.VARME_SUPPL_KODE AS Supplerende_varmeinstallation
	, Bygning.ETAGER_ANT AS Antal_etager
	, Bygning.BYG_BEBYG_ARL AS Bebygget_areal
	, Bygning.BYG_ARL_SAML AS Samlet_areal
	, Bygning.BYG_BOLIG_ARL_SAML AS Boligareal
	, Bygning.ERHV_ARL_SAML AS Erhvervsareal
	, Etage.K�lderareal_under_125cm as K�lderareal_under_125cm

	, Adgangsadresse.AdgAdr_id AS Adgangsadresse_id
	, Adgangsadresse.VejKode AS Vejkode
	, Adgangsadresse.VEJ_NAVN AS Vejnavn
	, Adgangsadresse.VejAdrNavn AS VejAdrNavn
	, Adgangsadresse.HUS_NR AS Husnummer
	, Adgangsadresse.PostNr AS Postnummer
	, Adgangsadresse.PostByNavn AS Bynavn
	, Adgangsadresse.SupBynavn AS Supplerende_bynavn
	, Adgangsadresse.KomKode AS Kommunekode
	, Adgangsadresse.MatrNr AS Matrikkelnummer

	, Adressepunkt.Adressepunkt_id AS Adressepunktsid
	, Adressepunkt.KoorSystem AS Koordinatsystem
	, Adressepunkt.KoorOest AS Longdetude
	, Adressepunkt.KoorNord AS Latitude


FROM BBR2017.dbo.CO40100T Bygning 
	LEFT MERGE JOIN @kaelderareal Etage ON Bygning.Bygning_id = Etage.Bygning_id
	LEFT JOIN BBR2017.dbo.CO42000T Adgangsadresse ON Bygning.AdgAdr_id = Adgangsadresse.AdgAdr_id
	INNER JOIN BBR2017.dbo.CO43200T Adressepunkt ON Adgangsadresse.Adressepunkt_id = Adressepunkt.Adressepunkt_id

WHERE 
	Bygning.KomKode = @kommunekode
	AND	Bygning.BYG_ANVEND_KODE < @Max_BYG_ANVEND_KODE
	AND	Bygning.BYG_ANVEND_KODE > 0
	AND Bygning.BYG_ARL_SAML > 0
	AND Bygning.OPFOERELSE_AAR > 0
	AND Bygning.ObjStatus = 1
	AND Etage.K�lderareal_under_125cm is not null
--ORDER BY Bygning.Bygning_id


Select
	@kommunekode AS Kommunekode
	, count(*) AS Antal_bygninger
	, sum(Bygning.BYG_BEBYG_ARL) AS Bebygget_areal
	, sum(Bygning.BYG_ARL_SAML) AS Samlet_areal
	, sum(Bygning.BYG_BOLIG_ARL_SAML) AS Boligareal
	, sum(Bygning.ERHV_ARL_SAML) AS Erhvervsareal
FROM BBR2017.dbo.CO40100T Bygning 
WHERE 
	Bygning.KomKode = @kommunekode
	AND	Bygning.BYG_ANVEND_KODE < @Max_BYG_ANVEND_KODE
	AND	Bygning.BYG_ANVEND_KODE > 0
	AND Bygning.BYG_ARL_SAML > 0
	AND Bygning.OPFOERELSE_AAR > 0


