declare @kommunekode int
declare @Max_BYG_ANVEND_KODE int
set @kommunekode = _kommunekode
set @Max_BYG_ANVEND_KODE = 600

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


