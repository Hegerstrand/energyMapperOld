
declare @kommunekode int
declare @Max_BYG_ANVEND_KODE int
set @kommunekode = _kommunekode
set @Max_BYG_ANVEND_KODE = 600




SELECT top(_top) Bygning.Bygning_id AS Bygningsid
	, Bygning.BYG_ANVEND_KODE AS Bygningsanvendelse
	, Bygning.OPFOERELSE_AAR AS Opfoerelsesaar
	, Bygning.OMBYG_AAR AS Ombygningsaar
	, Bygning.TAG_KODE AS Tagkode
	, Bygning.SuppTagDaekMat AS SuppTagDaekMat
	, Bygning.YDERVAEG_KODE AS Ydervaegkode
	, Bygning.SuppYderVaegMat AS SuppYderVaegMat
	, Bygning.VARMEINSTAL_KODE AS Varmeinstalationskode
	, Bygning.OPVARMNING_KODE AS Opvarmningskode
	, Bygning.VARME_SUPPL_KODE AS Supplerende_varmeinstallation
	, Bygning.ETAGER_ANT AS Antal_etager
	, Bygning.BYG_BEBYG_ARL AS Bebygget_areal
	, Bygning.BYG_ARL_SAML AS Samlet_areal
	, Bygning.BYG_BOLIG_ARL_SAML AS Boligareal
	, Bygning.ERHV_ARL_SAML AS Erhvervsareal
	, 0 as Kaelderareal_under_125cm

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
	, Adressepunkt.KoorOest AS X
	, Adressepunkt.KoorNord AS Y

FROM BBR2017.dbo.CO40100T Bygning
	LEFT JOIN BBR2017.dbo.CO42000T Adgangsadresse ON Bygning.AdgAdr_id = Adgangsadresse.AdgAdr_id
	INNER JOIN BBR2017.dbo.CO43200T Adressepunkt ON Adgangsadresse.Adressepunkt_id = Adressepunkt.Adressepunkt_id

WHERE
	Bygning.KomKode = @kommunekode
	AND	Bygning.BYG_ANVEND_KODE < @Max_BYG_ANVEND_KODE
	AND	Bygning.BYG_ANVEND_KODE > 0
	AND Bygning.BYG_ARL_SAML > 0
	AND Bygning.OPFOERELSE_AAR > 0
	AND Bygning.ObjStatus = 1
