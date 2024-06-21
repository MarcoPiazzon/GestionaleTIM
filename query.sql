/*Prendo tutti i contatti */
SELECT t.nome, t.cognome, t.email, t.tel, t.prefisso from Utente u join utentehacontatto uc on u.idUtente = uc.idUtente 
join contatto t on uc.idContatto = t.idContatto; 

/* 1.Ricerca cliente 2. Trattative cliente*/

SELECT c.indirizzoPrincipale, c.comunePrincipale, c.capProvinciale, c.ProvinciaDescPrincipale,
c.fisso, c.mobile, c.totale, c.fatturatoCerved FROM Cliente c where c.rag_soc_cli = $valore;


SELECT * from Trattative t where idCliente = $valore;
