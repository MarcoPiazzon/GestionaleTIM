-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Creato il: Lug 12, 2024 alle 12:50
-- Versione del server: 10.4.32-MariaDB
-- Versione PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `gestionale`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `andamentotrattativa`
--

CREATE TABLE `andamentotrattativa` (
  `idAndamento` int(11) NOT NULL,
  `nome` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `andamentotrattativa`
--

INSERT INTO `andamentotrattativa` (`idAndamento`, `nome`) VALUES
(1, 'IN TRATTATIVA'),
(2, 'VINTA'),
(3, 'PERSA');

-- --------------------------------------------------------

--
-- Struttura della tabella `appuntamento`
--

CREATE TABLE `appuntamento` (
  `idAppuntamento` int(11) NOT NULL,
  `idUtenteCreazione` int(11) NOT NULL,
  `titolo` varchar(255) DEFAULT NULL,
  `varieDiscussioni` varchar(255) DEFAULT NULL,
  `preventivoDaFare` varchar(255) DEFAULT NULL,
  `dataApp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `appuntamento`
--

INSERT INTO `appuntamento` (`idAppuntamento`, `idUtenteCreazione`, `titolo`, `varieDiscussioni`, `preventivoDaFare`, `dataApp`) VALUES
(37, 2, 'asd', '', '', '2024-07-16 15:48:00'),
(41, 2, 'Appuntamento diverso', 'dsfd', 'asd', '2024-07-21 19:33:00'),
(42, 2, 'Primo appuntamento', 'discussioni', 'Da far quesot', '2024-07-14 22:38:00'),
(44, 2, 'asdsad', 'dasdd', 'sad', '2024-07-16 15:45:00'),
(45, 2, 'ciao', 'dad', 'sad', '2024-07-27 15:45:00'),
(48, 15, 'Test da filippo', 'Sono filippo', 'Ho scritto un nuovo appuntamento', '2024-07-13 16:41:00');

-- --------------------------------------------------------

--
-- Struttura della tabella `categoria`
--

CREATE TABLE `categoria` (
  `idCategoria` int(11) NOT NULL,
  `nome` varchar(255) DEFAULT NULL,
  `descrizione` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `categoria`
--

INSERT INTO `categoria` (`idCategoria`, `nome`, `descrizione`) VALUES
(1, 'Licenze Google', 'Offerta Google WorkSpace (sia catena CRM/PRM sia TDS)'),
(2, 'Licenze Microsoft', 'Offerta Microsoft 365 (PRM/CRM e TDS) e altre licenze Microsoft (Sql Server, Dynamics 365, etc.) - specificare il tipo di licenze (365, Sql, etc.) nel campo \"Nome Opportunità\"'),
(3, 'Licenze - altro', 'Licenze sw di altri Vendor (non Google e non Microsoft): Veeam, etc. etc. - specificare il tipo di licenze (Veeam, etc.) nel campo \"Nome Opportunità\"'),
(7, 'Cloud TIM', 'Offerta TIM Cloud (TIM Cloud Flex, TIM Hosting Evoluto, TIM SDC, etc.), TIM Service Recovery, offerta DCS, etc. - specificare la offerta nel  campo \"Nome Opportunità\"'),
(8, 'Cloud Google', 'Offerta Google Cloud Platform'),
(9, 'Offerta Way', 'Offerte WAY: TIM Your WAY, Agritracker, etc. etc. - specificare la offerta nel  campo \"Nome Opportunità\"'),
(10, 'Offerta Omitech', 'Offerte Omitech: posta, servizi professionali, etc. - specificare la offerta nel  campo \"Nome Opportunità\"'),
(11, 'Offerta TXT/Ennova', 'Offerte di Ennova/TXT: Cisco Meraki, Skillo Sentinel, MDM, etc. - specificare la offerta nel  campo \"Nome Opportunità\"'),
(12, 'Offerta Noovle', 'Offerte di Servizi professionali, Salesforce, etc. - specificare la offerta nel  campo \"Nome Opportunità\"'),
(13, 'Offerta Telsy', 'Offerte Telsy (a listino o forntore): Telsy Skills, TIM Protezione dispositivi, TIM Risposta attacchi Cyber, etc. - specificare la offerta nel  campo \"Nome Opportunità\"'),
(14, 'Sicurezza altro', 'Offerte di Sicurezza a listino (MySecurityArea, offerte Swascan, etc.) o su base fornitore (es. Mead Informatica), ad esclusione delle offerte Telsy  - specificare la offerta nel  campo \"Nome Opportunità\"; in caso di offerte fornitore, specificare il forn'),
(15, 'TIM Digital Store altro', 'Offerte TDS non comprese nelle voci precedenti - specificare la offerta nel  campo \"Nome Opportunità\"'),
(16, 'Offerte fornitore/Listino altro', 'Offerte fornitore o a Listino non comprese nelle voci precedenti - specificare la offerta nel  campo \"Nome Opportunità\"; specificare il fornitore nel campo \"Fornitore\"');

-- --------------------------------------------------------

--
-- Struttura della tabella `cliente`
--

CREATE TABLE `cliente` (
  `idCliente` int(11) NOT NULL,
  `idUtente` int(11) NOT NULL,
  `idPortafoglio` int(11) NOT NULL,
  `tipoCliente` int(11) DEFAULT NULL,
  `cf` varchar(255) DEFAULT NULL,
  `ragioneSociale` varchar(255) DEFAULT NULL,
  `presidio` int(11) DEFAULT NULL,
  `indirizzoPrincipale` varchar(255) DEFAULT NULL,
  `comunePrincipale` int(11) DEFAULT NULL,
  `capPrincipale` varchar(255) DEFAULT NULL,
  `provinciaDescPrincipale` varchar(255) DEFAULT NULL,
  `provinciaSiglaPrincipale` varchar(255) DEFAULT NULL,
  `sediTot` int(11) DEFAULT NULL,
  `nLineeTot` int(11) DEFAULT NULL,
  `fisso` float DEFAULT NULL,
  `mobile` float DEFAULT NULL,
  `totale` float DEFAULT NULL,
  `fatturatoCerved` varchar(255) DEFAULT NULL,
  `clienteOffMobScadenza` varchar(255) DEFAULT NULL,
  `fatturatoTim` float DEFAULT NULL,
  `dipendenti` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `cliente`
--

INSERT INTO `cliente` (`idCliente`, `idUtente`, `idPortafoglio`, `tipoCliente`, `cf`, `ragioneSociale`, `presidio`, `indirizzoPrincipale`, `comunePrincipale`, `capPrincipale`, `provinciaDescPrincipale`, `provinciaSiglaPrincipale`, `sediTot`, `nLineeTot`, `fisso`, `mobile`, `totale`, `fatturatoCerved`, `clienteOffMobScadenza`, `fatturatoTim`, `dipendenti`) VALUES
(665, 2, 6, 1, '4679020232', 'ACCUDIRE SRL', 1, NULL, NULL, '37135', 'VERONA', 'VR', NULL, NULL, 0, 947.02, 947.02, '0', '0', NULL, NULL),
(666, 2, 6, 2, '4527300265', 'AGRIFUNG S.R.L. - SOCIETA  AGRICOLA', 2, 'None', NULL, 'None', NULL, NULL, 0, 0, 0, 0, 0, '500', '0.0', 0, 0),
(667, 2, 6, 3, '4734690284', 'ALBERTO DEL BIONDI S.P.A.', 1, 'VL. DELLA NAVIGAZIONE INTERNA 93', NULL, '35027', 'PADOVA', 'PD', 5, 43, 37403.2, 3862.06, 41265.3, '5466000', NULL, 8342, 47),
(668, 2, 6, 4, '4048610283', 'ALIFAX HOLDING S.P.A.', 1, 'V. FRANCESCO PETRARCA 2', NULL, '35020', 'PADOVA', 'PD', 1, 1, 0, 0, 0, '35781000', NULL, NULL, 2),
(669, 2, 6, 1, '1297140327', 'ALIFAX RESEARCH E DEVELOPMENT S.R.L', 1, NULL, NULL, '34149', 'TRIESTE', 'TS', NULL, NULL, 0, 2333.7, 2333.7, '0', '0', NULL, NULL),
(670, 2, 6, 3, '4337640280', 'ALIFAX S.R.L.', 1, 'V. FRANCESCO PETRARCA 2', NULL, '35020', 'PADOVA', 'PD', 5, 167, 8479.69, 39183.3, 47663, '52627000      ', '300', 45564, 56),
(671, 2, 6, 3, '2266211206', 'ANGOLOGIRO S.R.L.', 1, 'VL. MONTE GRAPPA 19', NULL, '31100', 'TREVISO', 'TV', 2, 5, 2774.6, 226.8, 3001.4, '3837000', NULL, 0, 22),
(672, 2, 6, 4, '2283330260', 'ANTONIO BASSO S.P.A.', 1, 'V. CASTAGNOLE 79', NULL, '31100', 'TREVISO', 'TV', 3, 4, 2200.21, 0, 2200.21, '29756000', NULL, 0, 84),
(673, 2, 6, 4, '3292680273', 'APV INVESTIMENTI S.P.A.', 1, 'V. DELL IDROGENO - MARGHERA 9', NULL, '30175', 'VENEZIA', 'VE', 2, 2, 4061.14, 0, 4061.14, '3279000', NULL, 140, 15),
(674, 2, 6, 2, '1944730264', 'AR.RE.FIN. S.R.L.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(675, 2, 6, 3, '94002080276', 'ARTEVEN - ASSOCIAZIONE REGIONALE PER LA PROMOZIONE E LA DIFFUSIONE DEL TEATRO E DELLA CULTURA NELLE', 1, 'V. GIOVANNI QUERINI - MESTRE 10', NULL, '30172', 'VENEZIA', 'VE', 2, 47, 0, 10397.9, 10397.9, '0', NULL, NULL, 15),
(676, 2, 6, 4, '1409020359', 'ARTI GRAFICHE REGGIANE & LAI S.P.A.', 1, 'V. DELL\'INDUSTRIA 19', NULL, '42025', 'REGGIO EMILIA', 'RE', 2, 4, 0, 0, 0, '217752000', NULL, NULL, 209),
(677, 2, 6, 1, '1703690303', 'ASSILAB GROUP SRL', 1, NULL, NULL, '33033', 'UDINE', 'UD', NULL, NULL, 253.14, 1783.74, 2036.88, '0', '0', NULL, NULL),
(678, 2, 6, 4, '80009140270', 'ASSOCIAZIONE VENEZIANA ALBERGATORI', 1, 'SESTIERE CANNAREGIO 3829', NULL, '30131', 'VENEZIA', 'VE', 8, 16, 5919.94, 0, 5919.94, '0', NULL, 0, NULL),
(679, 2, 6, 4, '1633400930', 'ATEX INDUSTRIES S.R.L.', 1, 'V. DELLE INDUSTRIE 2', NULL, '35010', 'PADOVA', 'PD', 2, 3, 2668.57, 3.93, 2672.5, '13903000', NULL, 0, 51),
(680, 2, 6, 2, '4126390279', 'ATHENA S.R.L.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(681, 2, 6, 3, '2206860278', 'BERENGO S.P.A.', 1, 'V. DELL\'ELETTRICITA\' - MESTRE 2', NULL, '30175', 'VENEZIA', 'VE', 7, 30, 25444.6, 2222.42, 27667, '39552000', NULL, 6086, 113),
(682, 2, 6, 2, '4068540261', 'BIO-HOUSE SRL', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(683, 2, 6, 3, '2037210271', 'CA  DA MOSTO S.P.A.', 1, 'V. VENEZIA 146', NULL, '30037', 'VENEZIA', 'VE', 7, 19, 39943.7, 1067.38, 41011.1, '27507000', NULL, 167, 91),
(684, 2, 6, 2, '3987541202', 'CARDUCCI STORE SRL', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(685, 2, 6, 1, '1730390265', 'CARTOPLASTICA S.R.L.', 1, NULL, NULL, '31030', 'TREVISO', 'TV', NULL, NULL, 0, 270, 270, '0', '0', NULL, NULL),
(686, 2, 6, 2, '3564180267', 'CENTRO SISTEMI S.R.L.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(687, 2, 6, 2, '152360301', 'CENTROFRUTTA CASTAGNOTTO DI CASTAGNOTTO S.& C.SAS', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(688, 2, 6, 3, '2092200340', 'CIVA GROUP DISTRIBUZIONE S.R.L.', 1, 'STR. NUOVA NAVIGLIO - PARADIGNA 6', NULL, '43100', 'PARMA', 'PR', 2, 13, 3788.57, 1881.72, 5670.29, '72479000', NULL, 0, 57),
(689, 2, 6, 4, '2793590270', 'CO.GE.S. DON LORENZO MILANI SOCIETA  COOPERATIVA SOCIALE', 1, 'V. PEZZANA 1', NULL, '30173', 'VENEZIA', 'VE', 3, 22, 17685.7, 25.93, 28363.6, '10466000', NULL, 0, 226),
(690, 2, 6, 3, '1954890263', 'CO.MET.FER. S.P.A.', 1, 'V. INTERPORTO 5', NULL, '30029', 'VENEZIA', 'VE', 3, 48, 15989.3, 24164.7, 40154, '212882000', NULL, 9546, 44),
(691, 2, 6, 2, '3407251200', 'COMACCHIO HEAVY EQUIPMENT SRL', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(692, 2, 6, 3, '2019450267', 'COMACCHIO S.P.A.', 1, 'V. CALLALTA 24/B', NULL, '31039', 'TREVISO', 'TV', 12, 112, 513073, 47002.7, 560076, '107467000', NULL, 421230, 220),
(693, 2, 6, 3, '2776570216', 'CON. FID. STATION SRL', 1, 'PL. PIETRO FAVRETTI - MESTRE 1', NULL, '30171', 'VENEZIA', 'VE', 10, 32, 9132.41, 2988.16, 12120.6, '11622000', NULL, 1164, 163),
(694, 2, 6, 4, '2877560215', 'CON.FID. LIVING SRL', 1, 'C. ITALIA%ITALIENALLEE 13/M', NULL, '39100', 'BOLZANO', 'BZ', 1, 1, 114.56, 0, 114.56, '1552000', NULL, 0, 0),
(695, 2, 6, 3, '1745940211', 'CON.FID. S.R.L.', 1, 'V. TONI EBNER%TONI EBNER - STRASSE 20', NULL, '39100', 'BOLZANO', 'BZ', 3, 19, 5230.09, 6353.85, 11584, '29340000', NULL, 130, 49),
(696, 2, 6, 3, '1538720267', 'CONSULSPED S.R.L.', 1, 'V. MARTIN LUTHER KING 8', NULL, '31032', 'TREVISO', 'TV', 8, 34, 55613.3, 969.63, 56583, '1444000', NULL, 14328, 6),
(697, 2, 6, 2, '1003690292', 'COOP. DELTARTISTI SOC. COOP. A R.L.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(698, 2, 6, 2, '323070268', 'COOPERATIVA G.A.I.V.I. GRUPPO ACQUISTI INSTALLATORI VENETI IDROTE RMOSANITARI - SOCIETA  COOPERATIVA', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(699, 2, 6, 2, '249660275', 'COOPERATIVA TRASBAGAGLI', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(700, 2, 6, 3, '343860276', 'CORPORAZIONE PILOTI DELL ESTUARIO VENETO', 1, 'STR. DELLA DROMA - LIDO 126', NULL, '30126', 'VENEZIA', 'VE', 4, 77, 23176.9, 12684.6, 35861.5, '0', NULL, 8970, 45),
(701, 2, 6, 3, '273100271', 'COSTAMPRESS S.P.A.', 1, 'V. G. TALIERCIO 13', NULL, '30037', 'VENEZIA', 'VE', 3, 44, 400000, 16339, 47985.7, '25410000 ', '0.0', 4766, 148),
(702, 2, 6, 2, '1639460268', 'COSTRUZIONI INDUSTRIALI CIVIDAC S.P.A.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(703, 2, 6, 2, '4997760287', 'CREATIVE TECHNOLOGICAL SOLUTION', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(704, 2, 6, 1, '4901240269', 'DAEFFE S.R.L.', 1, NULL, NULL, '31021', 'TREVISO', 'TV', NULL, NULL, 0, 317.78, 317.78, '0', '0', NULL, NULL),
(705, 2, 6, 3, '3716340272', 'DATIPHONE SRL', 1, 'V. PONTINA KM.29,100', NULL, '40', 'ROMA', 'RM', 2, 7, 1587.83, 832.87, 2420.71, '493000', NULL, 0, 4),
(706, 2, 6, 3, '5434590286', 'DESIGN BRAND ART SRL', 1, 'V. FORNACE MORANDI 24', NULL, '35133', 'PADOVA', 'PD', 1, 7, 4350.92, 2418.63, 6769.55, '1226000', NULL, 0, 7),
(707, 2, 6, 2, '4565050269', 'DOGE LOGISTICA SRL', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(708, 2, 6, 2, 'DROMHL62P30D578L', 'DORO MICHELE', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(709, 2, 6, 2, '3826701207', 'E. R. SERVICE SRLS', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(710, 2, 6, 3, '1009510288', 'EMI - MAGLIA S.P.A.', 1, 'V. LUPPIA SAN ZENO 21', NULL, '35044', 'PADOVA', 'PD', 5, 17, 15565, 832.71, 16397.7, '45783000', NULL, 2786, 147),
(711, 2, 6, 4, '1629560341', 'ERREA  SPORT S.P.A.', 1, 'STR. GIUSEPPE DI VITTORIO - SAN POLO 2/1', NULL, '43030', 'PARMA', 'PR', 1, 3, 0, 0, 0, '70033000', NULL, NULL, 140),
(712, 2, 6, 1, '3453800264', 'EUROTEC TECNOPOLIMERI SRL', 1, NULL, NULL, '31028', 'TREVISO', 'TV', NULL, NULL, 0, 2941.97, 2941.97, '0', '0', NULL, NULL),
(713, 2, 6, 4, '2169920374', 'FAAC PARTECIPAZIONI INDUSTRIALI S.R.L.', 1, 'V. PONTINA KM.29,100', NULL, '40', 'ROMA', 'RM', 2, 3, 0, 0, 0, '374173000', NULL, NULL, 0),
(714, 2, 6, 4, '3820731200', 'FAAC S.P.A.', 1, 'V. GIOVANNI BENINI 1', NULL, '40069', 'BOLOGNA', 'BO', 1, 1, 2535.68, 0, 2535.68, '146780000', NULL, 0, 426),
(715, 2, 6, 2, '2571200274', 'FIRAS S.R.L.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(716, 2, 6, 4, '3921060269', 'FLORICOLTURA CHIARA MARIO & FIGLI S.R.L.', 1, 'LG. PACIFICO VALUSSI 6', NULL, '33031', 'UDINE', 'UD', 1, 1, 655.82, 1282.29, 1938.11, '14902000', NULL, 0, 11),
(717, 2, 6, 3, '3502420262', 'FLORICOLTURA CHIARA MARIO E FIGLI SOCIETA  AGRICOLA S.S.', 1, 'V. MAGGIORE DI PIAVON 115', NULL, '31046', 'TREVISO', 'TV', 4, 20, 26006.6, 5690.55, 31697.2, '0', NULL, 2025, 44),
(718, 2, 6, 2, '4507230276', 'FRECCIA ROSSA SOCIETA  COOPERATIVA', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(719, 2, 6, 3, '3287700284', 'FUTURA RECUPERI S.R.L.', 1, 'V. CANOVE 4', NULL, '35010', 'PADOVA', 'PD', 1, 16, 3988.92, 2186.16, 6175.08, '5752000', NULL, 3138, 19),
(720, 2, 6, 1, '1216930261', 'G.D. DORIGO - S.P.A.', 1, NULL, NULL, '31053', 'TREVISO', 'TV', NULL, NULL, 19.35, 1512.39, 1531.74, '0', '0', NULL, NULL),
(721, 2, 6, 2, '6097140963', 'G.D.L. SERVICE SOC. COOP.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(722, 2, 6, 3, '3306860283', 'GAS.NET GROUP S.R.L.', 1, 'V. ROMA 1', NULL, '35020', 'PADOVA', 'PD', 4, 13, 56868.3, 2633.85, 59502.2, '1589000', NULL, 56204, 12),
(723, 2, 6, 4, '3511000279', 'GIACOMINI WINES SRL', 1, 'C. MARTIRI DELLA LIBERTA\' 113', NULL, '30026', 'VENEZIA', 'VE', 1, 1, 635.12, 2108.4, 2743.52, '3245000', NULL, 0, 5),
(724, 2, 6, 3, '1520440098', 'GIGLIO SOCIETA  A RESPONSABILITA  LIMITATA', 1, 'V. TRIESTINA 4', NULL, '30020', 'VENEZIA', 'VE', 4, 47, 1456.55, 28130.8, 29587.3, '15345000', NULL, 0, 52),
(725, 2, 6, 2, '3169800277', 'GRILLO PARLANTE SOCIETA  COOPERATIVA SOCIALE', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(726, 2, 6, 3, '902950278', 'GUARDIE AI FUOCHI DEL PORTO DI VENEZIA - SOCIETA  COOPERATIVA PER AZIONI  IN SIGLA  GUARDIE AI FUOCH', 1, 'V. FRATELLI BANDIERA - MESTRE 55', NULL, '30175', 'VENEZIA', 'VE', 4, 40, 24684.9, 6408.91, 31093.8, '5317000', NULL, 0, 62),
(727, 2, 6, 2, '1724210214', 'H&B RE S.R.L.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(728, 2, 6, 2, '4820850271', 'HELINEXT S.R.L.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(729, 2, 6, 4, '2692230218', 'HOLZNER & BERTAGNOLLI ENGINEERING SRL', 1, 'V. GUGLIELMO ZUCCONI 94', NULL, '41100', 'MODENA', 'MO', 1, 1, 1355.23, 0, 1355.23, '4100000', NULL, 0, 23),
(730, 2, 6, 3, '2636870285', 'HOTEL VILLA FRANCESCHI S.R.L.', 1, 'V. DON GIOVANNI MINZONI - MIRA PORTE 28', NULL, '30034', 'VENEZIA', 'VE', 6, 25, 15119.8, 4395.53, 19515.3, '2623000', NULL, 1131, 17),
(731, 2, 6, 3, '3820790230', 'HWG S.R.L.', 1, 'V. ENRICO FERMI 15', NULL, '37135', 'VERONA', 'VR', 2, 26, 1191.4, 31155.1, 32346.5, '11840000', NULL, 0, 56),
(732, 2, 6, 2, '4260590270', 'I.D. MARINE SRL', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(733, 2, 6, 2, '2383570278', 'IBIF S.R.L.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(734, 2, 6, 2, '2420040277', 'IDEAL LUX S.R.L.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(735, 2, 6, 3, '221480288', 'INARCA S.P.A.', 1, 'V. CA\' ZUSTO 35', NULL, '35010', 'PADOVA', 'PD', 2, 32, 24047.5, 4288.79, 28336.3, '36687000', NULL, 0, 121),
(736, 2, 6, 3, '202750287', 'INE SPA', 1, 'V. FACCA 10', NULL, '35013', 'PADOVA', 'PD', 4, 73, 46879.8, 15267.4, 62147.2, '43521000', NULL, 1048, 142),
(737, 2, 6, 4, '4660080286', 'INTELLIGENT SERVICE SRL', 1, 'V. PONTINA KM.29,100', NULL, '40', 'ROMA', 'RM', 1, 1, 491.95, 0, 491.95, '987000', NULL, 0, 3),
(738, 2, 6, 3, '1830880280', 'INTERPOLIMERI S.P.A.', 1, 'V. CASTELLAZZO 40', NULL, '20010', 'MILANO', 'MI', 3, 109, 1463.76, 43903.9, 45367.7, '425400000', NULL, 1417, 68),
(739, 2, 6, 2, '3627130267', 'K+', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(740, 2, 6, 2, '4312510268', 'KEESTRACK-IT S.R.L.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(741, 2, 6, 2, '3950380265', 'L.A.M.A. S.R.L.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(742, 2, 6, 3, '3923400265', 'LA CARTOTECNICA SRL', 1, 'V. ANTONIO GENTILIN 13', NULL, '31030', 'TREVISO', 'TV', 2, 20, 10965.9, 4327.31, 15293.2, '4812000', NULL, 0, 28),
(743, 2, 6, 2, '2389220274', 'LA GESTIONE S.R.L', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(744, 2, 6, 3, '1728000264', 'LA METANO TREVISO S.R.L.', 1, 'V. BIBANO 17', NULL, '31100', 'TREVISO', 'TV', 1, 12, 0, 1857.85, 1857.85, '5683000', NULL, NULL, 11),
(745, 2, 6, 2, '3228710277', 'LOGISTICA PAGGIOLA SRL', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(746, 2, 6, 2, '4331130270', 'M HOTELS SRL', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(747, 2, 6, 2, '4534640265', 'M SYMBOL GROUP S.R.L.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(748, 2, 6, 1, '626530265', 'M.I.D.A. - S.R.L.', 1, NULL, NULL, '31020', 'TREVISO', 'TV', NULL, NULL, 0, 2668.9, 2668.9, '0', '0', NULL, NULL),
(749, 2, 6, 2, '4182470262', 'MASTER S.R.L.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(750, 2, 6, 4, '6346211003', 'MB - SOCIETA A RESPONSABILITA  LIMITATA', 1, 'SESTIERE SAN MARCO - SAN MARCO 5010', NULL, '30124', 'VENEZIA', 'VE', 2, 2, 556.1, 0, 556.1, '395000', NULL, 0, 12),
(751, 2, 6, 2, '4181120264', 'MEDIA SPHAERA SRL', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(752, 2, 6, 3, '1843370261', 'MEET ITALIA SRL', 1, 'V. SILE 2/B', NULL, '31040', 'TREVISO', 'TV', 4, 9, 2990.1, 1678.91, 4669.01, '16712000', NULL, 120, 156),
(753, 2, 6, 2, '10580780962', 'MELITA ITALIA S.R.L.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(754, 2, 6, 3, '4378580262', 'MITO POLIMERI S.R.L.', 1, 'P. SAN VITALE 16', NULL, '36033', 'VICENZA', 'VI', 2, 44, 2556.22, 11302, 13858.2, '61544000', NULL, 0, 23),
(755, 2, 6, 1, '3884670278', 'MM-ONE GROUP S.R.L.', 1, NULL, NULL, '30020', 'VENEZIA', 'VE', NULL, NULL, 0, 4416.44, 4416.44, '0', '0', NULL, NULL),
(756, 2, 6, 4, '2403160266', 'MORATTO S.R.L.', 1, 'V. ALESSANDRO VOLTA 2', NULL, '31030', 'TREVISO', 'TV', 1, 1, 1280.84, 14.16, 1295, '17597000', NULL, 0, 60),
(757, 2, 6, 2, '1981270273', 'MULTI SERVICE S.R.L.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(758, 2, 6, 2, '4300140276', 'NOAH S.R.L.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(759, 2, 6, 3, '4152330264', 'O.M.I. TRE S.R.L.', 1, 'VL. DELL\'INDUSTRIA 14', NULL, '31055', 'TREVISO', 'TV', 1, 17, 8774.59, 785.52, 9560.11, '2916000', NULL, 3870, 4),
(760, 2, 6, 2, '5282830289', 'OMA NORD ENGINEERING & CONSTRUCTION SRL', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(761, 2, 6, 3, '2540210271', 'ONDULATI NORDEST S.P.A.', 1, 'V. DELLE INDUSTRIE 18', NULL, '30020', 'VENEZIA', 'VE', 1, 15, 735.8, 6644.33, 7380.13, '144680000', NULL, 0, 87),
(762, 2, 6, 3, '3942770276', 'OPEN SERVICE S.R.L.', 1, 'V. SEBASTIANO VENIER 5', NULL, '30020', 'VENEZIA', 'VE', 3, 109, 15792.2, 16898, 32690.2, '16674000', NULL, 9843, 785),
(763, 2, 6, 3, '612690271', 'OPERA SANTA MARIA DELLA CARITA', 1, 'SESTIERE SAN MARCO - SAN MARCO 1830', NULL, '30124', 'VENEZIA', 'VE', 10, 63, 37706.5, 4834.4, 42540.9, '0', NULL, 0, 364),
(764, 2, 6, 3, '2061320277', 'ORMESANI S.R.L.', 1, 'V. GIOVANNI PASCOLI 42', NULL, '30020', 'VENEZIA', 'VE', 3, 77, 23524.5, 15546.3, 39070.8, '70916000', NULL, 0, 78),
(765, 2, 6, 3, '2414650271', 'PAGAN ELETTROMECCANICA S.R.L.', 1, 'V. DELLA MECCANICA 8', NULL, '30100', 'VENEZIA', 'VE', 2, 17, 2724.91, 3742.2, 6467.11, '2458000', NULL, 0, 31),
(766, 2, 6, 3, '1975450279', 'PASTRELLO AUTOTRASPORTI S.R.L.', 1, 'V. DEL COMMERCIO - MESTRE 5', NULL, '30175', 'VENEZIA', 'VE', 4, 62, 13579.3, 14114.5, 27693.9, '18663000', NULL, 0, 25),
(767, 2, 6, 2, '3846660276', 'PELLETTERIA GRAZIELLA S.R.L.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(768, 2, 6, 4, '6258080966', 'PG MANAGEMENT S.R.L.', 1, 'SESTIERE SAN MARCO - SAN MARCO 3427', NULL, '30124', 'VENEZIA', 'VE', 1, 1, 6141.65, 0, 6141.65, '4939000', NULL, 6065, 54),
(769, 2, 6, 3, '767480262', 'PIVA - S.R.L.', 1, 'V. ROMA 149/B', NULL, '31050', 'TREVISO', 'TV', 1, 25, 17550.6, 2682.79, 20233.4, '10479000', NULL, 5914, 13),
(770, 2, 6, 3, '3565990268', 'PUNTO VERDE S.R.L.', 1, 'ZONA INDUSTRIALE 88', NULL, '31040', 'TREVISO', 'TV', 2, 38, 4794.24, 7481.39, 12275.6, '1683000', NULL, 2240, 30),
(771, 2, 6, 3, '4314190234', 'RBR ITALIA S.R.L.', 1, 'V. DELLE INDUSTRIE 2/D', NULL, '30020', 'VENEZIA', 'VE', 1, 8, 888, 845.69, 1733.69, '1112000', NULL, 0, 7),
(772, 2, 6, 3, '3094940230', 'RBR VERONA S.R.L', 1, 'V. MONSIGNORE GIACOMO GENTILIN 62', NULL, '37132', 'VERONA', 'VR', 1, 11, 768, 1507.69, 2275.69, '1532000', NULL, 0, 14),
(773, 2, 6, 4, '1873260309', 'RISCHIO S.R.L.', 1, 'V. LOVADINA 49', NULL, '31030', 'TREVISO', 'TV', 1, 2, 0, 2859.29, 2859.29, '6028000', NULL, NULL, 29),
(774, 2, 6, 4, '3933360285', 'S.I.T. S.R.L.', 1, 'FRAZ. ZUEL DI SOPRA 11', NULL, '32043', 'BELLUNO', 'BL', 1, 9, 225.09, 0, 225.09, '20816000', NULL, 0, 0),
(775, 2, 6, 4, '375680279', 'S.M.C. - SANTI MARINE CONSULTING S.R.L.', 1, 'V. TORINO - MESTRE 151/A', NULL, '30172', 'VENEZIA', 'VE', 1, 3, 0, 0, 0, '687000', NULL, NULL, 8),
(776, 2, 6, 2, '3561471206', 'SALCOM TECH S.R.L.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(777, 2, 6, 3, '2335540288', 'SALGAIM ECOLOGIC S.P.A.', 1, 'V. CRISTOFORO COLOMBO 1', NULL, '30010', 'VENEZIA', 'VE', 6, 36, 12965.9, 13774.2, 26740.1, '72988000', NULL, 234, 69),
(778, 2, 6, 2, '3366270266', 'SAN GREGORIO SOCIETA\' COOPERATIVA SOCIALE.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(779, 2, 6, 3, '16531491005', 'SCENARI IMMOBILIARI - ISTITUTO INDIPENDENTE DI STUDI RICERCHE, VALUTAZIONI E SISTEMI INFORMATIVI - S', 1, 'V. LOVANIO 4', NULL, '20121', 'MILANO', 'MI', 1, 29, 478.98, 16217.6, 16696.6, '2844000', NULL, 0, 11),
(780, 2, 6, 3, '1278710932', 'SEEK & PARTNERS S.P.A.', 1, 'V. JACOPO LINUSSIO 1', NULL, '33170', 'PORDENONE', 'PN', 1, 7, 2640.05, 39.45, 2679.5, '16594000', NULL, 0, 51),
(781, 2, 6, 2, '757650270', 'SILVA - SOCIETA  A RESPONSABILITA  LIMITATA', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(782, 2, 6, 2, '3696920267', 'SMARTY LAB S.R.L.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(783, 2, 6, 1, '3326980244', 'SOLARE MULTISERVICE SOCIETA  COOPERATIVA', 1, NULL, NULL, '36061', 'VICENZA', 'VI', NULL, NULL, 0, 310.84, 310.84, '0', '0', NULL, NULL),
(784, 2, 6, 3, '2079440265', 'SOPRIN - S.R.L.', 1, 'V. PONTINA KM.29,100', NULL, '40', 'ROMA', 'RM', 1, 39, 0, 36719.9, 36719.9, '4960000', NULL, NULL, 15),
(785, 2, 6, 4, '10556980158', 'SORIN GROUP ITALIA SRL', 1, 'V. STATALE NORD 86', NULL, '41037', 'MODENA', 'MO', 4, 33, 59500.9, 0, 59500.9, '225888000', NULL, 0, 825),
(786, 2, 6, 4, '3463030266', 'STUDIO NOTARILE ASSOCIATO BARAVELLI - BIANCONI - TALICE', 1, 'V. SILVIO PELLICO 1', NULL, '31100', 'TREVISO', 'TV', 1, 4, 5380.92, 0, 5380.92, '0', NULL, 0, NULL),
(787, 2, 6, 2, '4994120261', 'SUPERMERCATI ZANOTTO SNC DI ZANOTTO ALEX E PILLON PARIDE', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(788, 2, 6, 3, '2057670271', 'TARGET MOTIVATION S.R.L.', 1, 'V. TORINO - MESTRE 151/E', NULL, '30172', 'VENEZIA', 'VE', 2, 33, 6265.15, 6192.58, 12457.7, '8730000', NULL, 3453, 13),
(789, 2, 6, 3, '1711410249', 'TELERADIO DIFFUSIONE BASSANO S.R.L.', 1, 'V. MARCO MELCHIORAZZO 7', NULL, '36061', 'VICENZA', 'VI', 2, 25, 1031, 1254.33, 2285.33, '3656000', NULL, 0, 75),
(790, 2, 6, 3, '3828090278', 'TERRE DI VENEZIA S.R.L.', 1, 'ISOLA DI MAZZORBO - BURANO 3', NULL, '30142', 'VENEZIA', 'VE', 2, 12, 8592.44, 1146.27, 9738.71, '3156000', NULL, 5333, 51),
(791, 2, 6, 2, '2937720270', 'TRAMONTE ELETTROIMPIANTI ENGINEERING SRL', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(792, 2, 6, 4, '4207510241', 'U-KEG GROUP S.R.L.', 1, 'V. FORESTO SUD 1', NULL, '31025', 'TREVISO', 'TV', 1, 7, 7577.84, 0, 7577.84, '1637000', NULL, 0, 7),
(793, 2, 6, 3, '3339790275', 'UNIONE AGRICOLTORI VENEZIA S.R.L.', 1, 'V. CLAUDIO MONTEVERDI - MESTRE 15', NULL, '30174', 'VENEZIA', 'VE', 14, 56, 19652.3, 3372.76, 23025.1, '1866000', NULL, 0, 36),
(794, 2, 6, 3, '299420273', 'VETRERIA ARTISTICA ARCHIMEDE SEGUSO S.R.L.', 1, 'FDM. SERENELLA - MURANO 18', NULL, '30141', 'VENEZIA', 'VE', 4, 31, 7083.64, 5423.91, 12507.5, '970000', NULL, 0, 9),
(795, 2, 6, 2, '1859540260', 'VISARD S.R.L.', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(796, 2, 3, NULL, '', 'Sono un nuovo cliente', NULL, '', NULL, '', NULL, NULL, 0, 0, 0, 0, 0, '', '', 0, 0),
(797, 2, 3, NULL, '', 'sono un nuovo cliente', NULL, '', NULL, '', NULL, NULL, 0, 0, 0, 0, 0, '', '', 0, 0),
(798, 2, 3, NULL, '', 'Sdrogo totale', NULL, '', NULL, '', NULL, NULL, 0, 0, 0, 0, 0, '', '', 0, 0),
(799, 2, 6, NULL, '', 'Sdrogo totale', NULL, '', NULL, '', NULL, NULL, 0, 0, 0, 0, 0, '', '', 0, 0),
(800, 2, 6, NULL, '', 'test', NULL, '', NULL, '', NULL, NULL, 0, 0, 0, 0, 0, '', '', 0, 0),
(801, 2, 6, NULL, 'dasd', 'sadsa', NULL, '', NULL, '', NULL, NULL, 0, 0, 0, 0, 45.8, '', '', 45597, 0);

-- --------------------------------------------------------

--
-- Struttura della tabella `clienteappuntamento`
--

CREATE TABLE `clienteappuntamento` (
  `idCliente` int(11) NOT NULL,
  `idAppuntamento` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `comune`
--

CREATE TABLE `comune` (
  `idComune` int(11) NOT NULL,
  `nome` varchar(255) DEFAULT NULL,
  `sigla` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `contatto`
--

CREATE TABLE `contatto` (
  `idContatto` int(11) NOT NULL,
  `idUtente` int(11) NOT NULL,
  `nome` varchar(255) DEFAULT NULL,
  `secondoNome` varchar(255) DEFAULT NULL,
  `cognome` varchar(255) DEFAULT NULL,
  `viaUfficio1` varchar(255) DEFAULT NULL,
  `viaUfficio2` varchar(255) DEFAULT NULL,
  `viaUfficio3` varchar(255) DEFAULT NULL,
  `citta` varchar(255) DEFAULT NULL,
  `provincia` varchar(255) DEFAULT NULL,
  `cap` varchar(255) DEFAULT NULL,
  `numUfficio` varchar(255) DEFAULT NULL,
  `numUfficio2` varchar(255) DEFAULT NULL,
  `telefonoPrincipale` varchar(255) DEFAULT NULL,
  `faxAbitazione` varchar(255) DEFAULT NULL,
  `abitazione` varchar(255) DEFAULT NULL,
  `abitazione2` varchar(255) DEFAULT NULL,
  `cellulare` varchar(255) DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `numeroID` varchar(255) DEFAULT NULL,
  `paginaWeb` varchar(255) DEFAULT NULL,
  `email1` varchar(255) DEFAULT NULL,
  `email2` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `contatto`
--

INSERT INTO `contatto` (`idContatto`, `idUtente`, `nome`, `secondoNome`, `cognome`, `viaUfficio1`, `viaUfficio2`, `viaUfficio3`, `citta`, `provincia`, `cap`, `numUfficio`, `numUfficio2`, `telefonoPrincipale`, `faxAbitazione`, `abitazione`, `abitazione2`, `cellulare`, `note`, `numeroID`, `paginaWeb`, `email1`, `email2`) VALUES
(1, 2, 'Assistenza', '', 'Ariston ', '', '', '', NULL, '', '', '', '', '', '', '3466875043 ', NULL, '041 987554', '', '', '', 'dasd@gmail.com', ''),
(2, 2, 'Paolo', '', 'Mugnaini ', '', '', '', NULL, '', '', '', '', '', '', '', NULL, '392 365 9397', '', '', '', '', ''),
(3, 2, 'Pompeo', 'Avv', 'Pierovalentina', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '+393755418470', NULL, NULL, NULL, 'riccardo.pompeo@pierodellavalentina.com', NULL),
(4, 2, 'Router', NULL, 'Zyxel', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Account\nadmin\nadmin', NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Struttura della tabella `partecipanti`
--

CREATE TABLE `partecipanti` (
  `idAppuntamento` int(11) NOT NULL,
  `idUtente` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struttura della tabella `portafoglio`
--

CREATE TABLE `portafoglio` (
  `idPortafoglio` int(11) NOT NULL,
  `idUtente` int(11) NOT NULL,
  `dataInserimento` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `portafoglio`
--

INSERT INTO `portafoglio` (`idPortafoglio`, `idUtente`, `dataInserimento`) VALUES
(6, 2, '2024-06-29');

-- --------------------------------------------------------

--
-- Struttura della tabella `presidio`
--

CREATE TABLE `presidio` (
  `idPresidio` int(11) NOT NULL,
  `nome` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `presidio`
--

INSERT INTO `presidio` (`idPresidio`, `nome`) VALUES
(1, 'PRESIDIO CB'),
(2, 'PROSPECT');

-- --------------------------------------------------------

--
-- Struttura della tabella `tipocliente`
--

CREATE TABLE `tipocliente` (
  `idTipoCliente` int(11) NOT NULL,
  `nome` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `tipocliente`
--

INSERT INTO `tipocliente` (`idTipoCliente`, `nome`) VALUES
(1, 'MOBILE'),
(2, 'NO_CONS'),
(3, 'COMUNE'),
(4, 'FISSO');

-- --------------------------------------------------------

--
-- Struttura della tabella `trattativa`
--

CREATE TABLE `trattativa` (
  `idTrattativa` int(11) NOT NULL,
  `idUtente` int(11) DEFAULT NULL,
  `idCliente` int(11) DEFAULT NULL,
  `codiceCtrDigitali` varchar(255) DEFAULT NULL,
  `codiceSalesHub` varchar(255) DEFAULT NULL,
  `areaManager` varchar(255) DEFAULT NULL,
  `zona` varchar(255) DEFAULT NULL,
  `tipo` varchar(255) DEFAULT NULL,
  `nomeOpportunita` varchar(255) DEFAULT NULL,
  `dataCreazioneOpportunita` date DEFAULT current_timestamp(),
  `fix` float DEFAULT NULL,
  `mobile` double DEFAULT NULL,
  `categoriaOffertaIT` int(11) DEFAULT NULL,
  `it` float DEFAULT NULL,
  `lineeFoniaFix` float DEFAULT NULL,
  `aom` float DEFAULT NULL,
  `mnp` float DEFAULT NULL,
  `al` float DEFAULT NULL,
  `dataChiusura` date DEFAULT NULL,
  `fase` int(11) DEFAULT NULL,
  `noteSpecialista` varchar(255) DEFAULT NULL,
  `probabilita` int(11) DEFAULT NULL,
  `inPaf` tinyint(1) DEFAULT NULL,
  `record` int(11) DEFAULT NULL,
  `fornitore` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `trattativa`
--

INSERT INTO `trattativa` (`idTrattativa`, `idUtente`, `idCliente`, `codiceCtrDigitali`, `codiceSalesHub`, `areaManager`, `zona`, `tipo`, `nomeOpportunita`, `dataCreazioneOpportunita`, `fix`, `mobile`, `categoriaOffertaIT`, `it`, `lineeFoniaFix`, `aom`, `mnp`, `al`, `dataChiusura`, `fase`, `noteSpecialista`, `probabilita`, `inPaf`, `record`, `fornitore`) VALUES
(102, 2, 670, 'None', 'None', 'DEL DEGAN', 'VENETO', 'PRESIDIO CB', 'nici top 2 sedi altro olo 123', '2023-01-23', 15000, 25, 3, 0, 0, 0, 0, 0, '2024-05-09', 2, 'in corso', 65, 0, 1, 'None'),
(127, 2, 670, 'None', 'None', 'DEL DEGAN', 'VENETO', 'PRESIDIO CB', 'nici top 2 sedi rientro altro olo', '2023-01-23', 15000, 0, 14, 0, 0, 0, 0, 0, '2024-05-01', 1, 'in corso', 90, 0, 1, 'None'),
(128, 2, 667, '3928792', 'ex 3087933 3928792', 'DEL DEGAN', 'VENETO', 'PRESIDIO CB', 'ftto + vdsl bu', '0000-00-00', 9819, 0, 7, NULL, NULL, NULL, 45, NULL, '2024-02-29', 2, NULL, 100, NULL, 2, NULL),
(129, 2, 681, 'None', 'None', 'DEL DEGAN', 'VENETO', 'PRESIDIO CB', '3 sim e trunk', '2023-01-23', 5000, 0, 1, 0, 0, 0, 0, 0, '2024-07-25', 2, 'None', 30, 0, 3, 'None');

--
-- Trigger `trattativa`
--
DELIMITER $$
CREATE TRIGGER `after_trattativa_insert` AFTER INSERT ON `trattativa` FOR EACH ROW BEGIN
    IF (NEW.codiceCtrDigitali IS NULL AND NEW.codiceSalesHub is null and NEW.areaManager is null and new.zona is null and new.tipo is null 
        and new.nomeOpportunita is null and new.dataCreazioneOpportunita is null and new.fix is null and new.mobile is null and new.categoriaOffertaIT is null 
        and new.it is null and new.lineeFoniaFix is null and new.aom is null and new.mnp is null and new.al is null and new.dataChiusura is null 
        and new.fase is null and new.noteSpecialista is null and new.probabilita is null and new.inPaf is null and new.record is null and new.fornitore is null) THEN
    	SIGNAL sqlstate '45001' set message_text = "No way ! You cannot do this !";
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Struttura della tabella `trattativaappuntamento`
--

CREATE TABLE `trattativaappuntamento` (
  `idTrattativa` int(11) NOT NULL,
  `idAppuntamento` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `trattativaappuntamento`
--

INSERT INTO `trattativaappuntamento` (`idTrattativa`, `idAppuntamento`) VALUES
(128, 37),
(127, 41),
(0, 42),
(0, 44),
(0, 45),
(0, 48);

-- --------------------------------------------------------

--
-- Struttura della tabella `utente`
--

CREATE TABLE `utente` (
  `idUtente` int(11) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `cognome` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `psw` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dump dei dati per la tabella `utente`
--

INSERT INTO `utente` (`idUtente`, `nome`, `cognome`, `email`, `psw`) VALUES
(2, 'Marco', 'Piazzon', 'mp@gmail.com', '$2b$12$sNEprcMjxKXYpqF6Fmbol.8hBP2KeWNM9WWjPb.ozsgsw4PQJXPHC'),
(15, 'Filippo', 'Iaccarino', 'filippo@gmail.com', '$2b$12$WvdLXC8usoo67U2LE/QIM.BAY0RfGRoAQ7dkg6Va.J8nIw/XY7aL.');

-- --------------------------------------------------------

--
-- Struttura della tabella `utentehacontatto`
--

CREATE TABLE `utentehacontatto` (
  `idUtente` int(11) NOT NULL,
  `idContatto` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `andamentotrattativa`
--
ALTER TABLE `andamentotrattativa`
  ADD PRIMARY KEY (`idAndamento`);

--
-- Indici per le tabelle `appuntamento`
--
ALTER TABLE `appuntamento`
  ADD PRIMARY KEY (`idAppuntamento`),
  ADD KEY `idUtenteCreazione` (`idUtenteCreazione`);

--
-- Indici per le tabelle `categoria`
--
ALTER TABLE `categoria`
  ADD PRIMARY KEY (`idCategoria`);

--
-- Indici per le tabelle `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`idCliente`),
  ADD KEY `idUtente` (`idUtente`),
  ADD KEY `idPortafoglio` (`idPortafoglio`),
  ADD KEY `tipoCliente` (`tipoCliente`),
  ADD KEY `presidio` (`presidio`),
  ADD KEY `comunePrincipale` (`comunePrincipale`);

--
-- Indici per le tabelle `clienteappuntamento`
--
ALTER TABLE `clienteappuntamento`
  ADD KEY `idCliente` (`idCliente`),
  ADD KEY `idAppuntamento` (`idAppuntamento`);

--
-- Indici per le tabelle `comune`
--
ALTER TABLE `comune`
  ADD PRIMARY KEY (`idComune`);

--
-- Indici per le tabelle `contatto`
--
ALTER TABLE `contatto`
  ADD PRIMARY KEY (`idContatto`);

--
-- Indici per le tabelle `partecipanti`
--
ALTER TABLE `partecipanti`
  ADD KEY `idAppuntamento` (`idAppuntamento`),
  ADD KEY `idUtente` (`idUtente`);

--
-- Indici per le tabelle `portafoglio`
--
ALTER TABLE `portafoglio`
  ADD PRIMARY KEY (`idPortafoglio`),
  ADD KEY `FK_Utente` (`idUtente`);

--
-- Indici per le tabelle `presidio`
--
ALTER TABLE `presidio`
  ADD PRIMARY KEY (`idPresidio`);

--
-- Indici per le tabelle `tipocliente`
--
ALTER TABLE `tipocliente`
  ADD PRIMARY KEY (`idTipoCliente`);

--
-- Indici per le tabelle `trattativa`
--
ALTER TABLE `trattativa`
  ADD PRIMARY KEY (`idTrattativa`),
  ADD KEY `idUtente` (`idUtente`),
  ADD KEY `idCliente` (`idCliente`),
  ADD KEY `zona` (`zona`),
  ADD KEY `categoriaOffertaIT` (`categoriaOffertaIT`),
  ADD KEY `fase` (`fase`);

--
-- Indici per le tabelle `trattativaappuntamento`
--
ALTER TABLE `trattativaappuntamento`
  ADD KEY `trattativaappuntamento_ibfk_1` (`idTrattativa`),
  ADD KEY `trattativaappuntamento_ibfk_2` (`idAppuntamento`);

--
-- Indici per le tabelle `utente`
--
ALTER TABLE `utente`
  ADD PRIMARY KEY (`idUtente`);

--
-- Indici per le tabelle `utentehacontatto`
--
ALTER TABLE `utentehacontatto`
  ADD KEY `idUtente` (`idUtente`),
  ADD KEY `idContatto` (`idContatto`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `andamentotrattativa`
--
ALTER TABLE `andamentotrattativa`
  MODIFY `idAndamento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT per la tabella `appuntamento`
--
ALTER TABLE `appuntamento`
  MODIFY `idAppuntamento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT per la tabella `categoria`
--
ALTER TABLE `categoria`
  MODIFY `idCategoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT per la tabella `cliente`
--
ALTER TABLE `cliente`
  MODIFY `idCliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=802;

--
-- AUTO_INCREMENT per la tabella `comune`
--
ALTER TABLE `comune`
  MODIFY `idComune` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `contatto`
--
ALTER TABLE `contatto`
  MODIFY `idContatto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT per la tabella `portafoglio`
--
ALTER TABLE `portafoglio`
  MODIFY `idPortafoglio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT per la tabella `presidio`
--
ALTER TABLE `presidio`
  MODIFY `idPresidio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT per la tabella `tipocliente`
--
ALTER TABLE `tipocliente`
  MODIFY `idTipoCliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT per la tabella `trattativa`
--
ALTER TABLE `trattativa`
  MODIFY `idTrattativa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=131;

--
-- AUTO_INCREMENT per la tabella `utente`
--
ALTER TABLE `utente`
  MODIFY `idUtente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `appuntamento`
--
ALTER TABLE `appuntamento`
  ADD CONSTRAINT `appuntamento_ibfk_2` FOREIGN KEY (`idUtenteCreazione`) REFERENCES `utente` (`idUtente`);

--
-- Limiti per la tabella `cliente`
--
ALTER TABLE `cliente`
  ADD CONSTRAINT `cliente_ibfk_1` FOREIGN KEY (`idUtente`) REFERENCES `utente` (`idUtente`),
  ADD CONSTRAINT `cliente_ibfk_3` FOREIGN KEY (`tipoCliente`) REFERENCES `tipocliente` (`idTipoCliente`),
  ADD CONSTRAINT `cliente_ibfk_4` FOREIGN KEY (`presidio`) REFERENCES `presidio` (`idPresidio`),
  ADD CONSTRAINT `cliente_ibfk_5` FOREIGN KEY (`comunePrincipale`) REFERENCES `comune` (`idComune`);

--
-- Limiti per la tabella `clienteappuntamento`
--
ALTER TABLE `clienteappuntamento`
  ADD CONSTRAINT `clienteappuntamento_ibfk_1` FOREIGN KEY (`idCliente`) REFERENCES `cliente` (`idCliente`),
  ADD CONSTRAINT `clienteappuntamento_ibfk_2` FOREIGN KEY (`idAppuntamento`) REFERENCES `appuntamento` (`idAppuntamento`);

--
-- Limiti per la tabella `partecipanti`
--
ALTER TABLE `partecipanti`
  ADD CONSTRAINT `partecipanti_ibfk_1` FOREIGN KEY (`idAppuntamento`) REFERENCES `appuntamento` (`idAppuntamento`),
  ADD CONSTRAINT `partecipanti_ibfk_2` FOREIGN KEY (`idUtente`) REFERENCES `utente` (`idUtente`);

--
-- Limiti per la tabella `trattativa`
--
ALTER TABLE `trattativa`
  ADD CONSTRAINT `trattativa_ibfk_1` FOREIGN KEY (`idUtente`) REFERENCES `utente` (`idUtente`),
  ADD CONSTRAINT `trattativa_ibfk_2` FOREIGN KEY (`idCliente`) REFERENCES `cliente` (`idCliente`),
  ADD CONSTRAINT `trattativa_ibfk_4` FOREIGN KEY (`categoriaOffertaIT`) REFERENCES `categoria` (`idCategoria`),
  ADD CONSTRAINT `trattativa_ibfk_5` FOREIGN KEY (`fase`) REFERENCES `andamentotrattativa` (`idAndamento`);

--
-- Limiti per la tabella `utentehacontatto`
--
ALTER TABLE `utentehacontatto`
  ADD CONSTRAINT `utentehacontatto_ibfk_1` FOREIGN KEY (`idUtente`) REFERENCES `utente` (`idUtente`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
