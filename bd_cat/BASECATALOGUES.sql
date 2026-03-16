ALTER TABLE catalogues_accounttype COLLATE='utf8_general_ci';
INSERT INTO catalogues_accounttype (account_type) VALUES
('Débito'),
('Crédito');

ALTER TABLE catalogues_activitytype COLLATE='utf8_general_ci';
INSERT INTO catalogues_activitytype (activity_number, activity_description, type) VALUES 
('1001', 'Accesorios Covid 19', 1),
('1002', 'Accesorios para Vehículos', 1),
('1003', 'Alimentos y Bebidas', 1),
('1004', 'Animales y Mascotas', 1),
('1005', 'Autos, Motos y Otros', 1),
('1006', 'Artículos para Fumadores', 1),
('1007', 'Belleza y Cuidado Personal', 1),
('1008', 'Cámaras y Accesorios', 1),
('1009', 'Celulares y Accesorios', 1),
('1010', 'Computación', 1),
('1011', 'Deportes y Fitness', 1),
('1012', 'Electrodomésticos', 1),
('1013', 'Electrónica, Audio y Video', 1),
('1014', 'Material de Construcción', 1),
('1015', 'Hogar, Muebles y Jardín', 1),
('1016', 'Industrias y Oficinas', 1),
('1017', 'Papelería y Mercería', 1),
('1018', 'Pirotecnia', 1),
('1019', 'Instrumentos Musicales', 1),
('1020', 'Joyas y Relojes', 1),
('1021', 'Juegos y Juguetes', 1),
('1022', 'Libros, Revistas y Comics', 1),
('1023', 'Ropa, Calzado y Bisutería', 1),
('1024', 'Salud y Equipamiento Médico', 1),
('1025', 'Suplementos Alimenticios', 1),
('1026', 'Otros', 1),
('2001', 'Agente Inmobiliario', 2),
('2002', 'Arquitectura', 2),
('2003', 'Belleza y Cuidado Personal', 2),
('2004', 'Contable y Fiscal', 2),
('2005', 'Clases, Cursos y Capacitaciones', 2),
('2006', 'Diseño páginas Web', 2),
('2007', 'Estudio Fotográfico', 2),
('2008', 'Fiestas y Eventos', 2),
('2009', 'Financiero Créditos', 2),
('2010', 'Financiero Inversiones', 2),
('2011', 'Financiero Fideicomisos', 2),
('2012', 'Legal', 2),
('2013', 'Medico', 2),
('2014', 'Mercadotecnia y Publicidad', 2), 
('2015', 'Mantenimiento y Reparación', 2),
('2016', 'Automotriz', 2), 
('2017', 'Hogar', 2),
('2018', 'Computadoras', 2),
('2019', 'Celulares', 2),
('2020', 'Programación de Apps', 2);

ALTER TABLE catalogues_affiliatetype COLLATE='utf8_general_ci';
INSERT INTO catalogues_affiliatetype (affiliate_type)
VALUES
('Afiliado IMSS'),
('Promotor SC'),
('Ambas');

ALTER TABLE catalogues_affiliationreason COLLATE='utf8_general_ci';
INSERT INTO catalogues_affiliationreason (affiliattion_reason)
VALUES
('Seguridad social'),
('Ley 73'),
('Ley 97'),
('Promotor'),
('Página web');

ALTER TABLE catalogues_bnknames COLLATE='utf8_general_ci';
INSERT INTO catalogues_bnknames (bnk_name)
VALUES
('Banco Nacional de México (Banamex)'),
('Banco Santander (México)'),
('HSBC México'),
('Scotiabank Inverlat'),
('BBVA Bancomer'),
('Banco Mercantil del Norte (Banorte)'),
('Banco Interacciones'),
('Banco Inbursa'),
('banca Mifel'),
('Banco Regional de Monterrey'),
('Banco Invex'),
('Banco del Bajio'),
('Bansi'),
('Banca Afirme'),
('Bank of America México'),
('Banco JP Morgan'),
('Banco Ve Por Mas'),
('American Express Bank (México)'),
('Investa Bank'),
('CiBanco'),
('Bank of Tokyo-Mitsubishi UFJ (México)'),
('Banco Monex'),
('Deutsche Bank México'),
('Banco Azteca'),
('Banco Credit Suisse (México)'),
('Banco Autofin México'),
('Barclays Bank México'),
('Banco Ahorro Famsa'),
('Intercam Banco'),
('ABC Capital '),
('Banco Actinver'),
('Banco Compartamos'),
('Banco Multiva'),
('UBS Bank México'),
('Bancoppel'),
('ConsuBanco'),
('Banco Wal-Mart de México'),
('Volkswagen Bank'),
('Banco Base'),
('Banco Pagatodo'),
('Banco Forjadores'),
('Bankaool'),
('Banco Inmobiliario Mexicano'),
('Fundación Dondé Banco'),
('Banco Bancrea');

ALTER TABLE catalogues_dependentactivity COLLATE='utf8_general_ci';
INSERT INTO catalogues_dependentactivity (dependent_activity)
VALUES
('Ama de casa'),
('Estudiante'),
('Retirado'),
('Incapacitado'),
('Otro');

ALTER TABLE catalogues_dependentrelation COLLATE='utf8_general_ci';
INSERT INTO catalogues_dependentrelation (relation) 
VALUES
('Esposo(a)'),
('Conyuge'),
('Hijo'),
('Padre'),
('Madre'),
('Otro');

ALTER TABLE catalogues_maritalstatus COLLATE='utf8_general_ci';
INSERT INTO catalogues_maritalstatus (marital_status) 
VALUES
('Soltero'),
('Casado'),
('Divorciado'),
('Viudo'),
('Unión libre');

ALTER TABLE catalogues_matrimonialregime COLLATE='utf8_general_ci';
INSERT INTO catalogues_matrimonialregime (matrimonial_regime) 
VALUES
('Sociedad conyugal'),
('Separación de bienes'),
('Participación en los gananciales'),
('No aplica');

ALTER TABLE catalogues_natiolanities COLLATE='utf8_general_ci';
INSERT INTO catalogues_natiolanities (nationality) 
VALUES
('NAMIBIANA'),
('ANGOLESA'),
('ARGELIANA'),
('DE BENNIN'),
('BOTSWANESA'),
('BURUNDESA'),
('DE CABO VERDE'),
('COMORENSE'),
('CONGOLESA'),
('MARFILEÑA'),
('CHADIANA'),
('DE DJIBOUTI'),
('EGIPCIA'),
('ETIOPE'),
('GABONESA'),
('GAMBIANA'),
('GHANATA'),
('GUINEA'),
('GUINEA'),
('GUINEA ECUATORIANA'),
('LIBIA'),
('KENIANA'),
('LESOTHENSE'),
('LIBERIANA'),
('MALAWIANA'),
('MALIENSE'),
('MARROQUI'),
('MAURICIANA'),
('MAURITANA'),
('MOZAMBIQUEÑA'),
('NIGERINA'),
('NIGERIANA'),
('CENTRO AFRICANA'),
('CAMERUNESA'),
('TANZANIANA'),
('RWANDESA'),
('DEL SAHARA'),
('DE SANTO TOME'),
('SENEGALESA'),
('DE SEYCHELLES'),
('SIERRA LEONESA'),
('SOMALI'),
('SUDAFRICANA'),
('SUDANESA'),
('SWAZI'),
('TOGOLESA'),
('TUNECINA'),
('UGANDESA'),
('ZAIRANA'),
('ZAMBIANA'),
('DE ZIMBAWI'),
('ARGENTINA'),
('BAHAMEÑA'),
('DE BARBADOS'),
('BELICEÑA'),
('BOLIVIANA'),
('BRASILEÑA'),
('CANADIENSE'),
('COLOMBIANA'),
('COSTARRICENSE'),
('CUBANA'),
('CHILENA'),
('DOMINICA'),
('SALVADOREÑA'),
('ESTADOUNIDENSE'),
('GRANADINA'),
('GUATEMALTECA'),
('BRITANICA'),
('GUYANESA'),
('HAITIANA'),
('HONDUREÑA'),
('JAMAIQUINA'),
('MEXICANA'),
('NICARAGUENSE'),
('PANAMEÑA'),
('PARAGUAYA'),
('PERUANA'),
('PUERTORRIQUEÑA'),
('DOMINICANA'),
('SANTA LUCIENSE'),
('SURINAMENSE'),
('TRINITARIA'),
('URUGUAYA'),
('VENEZOLANA'),
('AMERICANA'),
('AFGANA'),
('DE BAHREIN'),
('BHUTANESA'),
('BIRMANA'),
('NORCOREANA'),
('SUDCOREANA'),
('CHINA'),
('CHIPRIOTA'),
('ARABE'),
('FILIPINA'),
('HINDU'),
('INDONESA'),
('IRAQUI'),
('IRANI'),
('ISRAELI'),
('JAPONESA'),
('JORDANA'),
('CAMBOYANA'),
('KUWAITI'),
('LIBANESA'),
('MALASIA'),
('MALDIVA'),
('MONGOLESA'),
('NEPALESA'),
('OMANESA'),
('PAKISTANI'),
('DEL QATAR'),
('SIRIA'),
('LAOSIANA'),
('SINGAPORENSE'),
('TAILANDESA'),
('TAIWANESA'),
('TURCA'),
('NORVIETNAMITA'),
('YEMENI'),
('ALBANESA'),
('ALEMANA'),
('ANDORRANA'),
('AUSTRIACA'),
('BELGA'),
('BULGARA'),
('CHECOSLOVACA'),
('DANESA'),
('VATICANA'),
('ESPAÑOLA'),
('FINLANDESA'),
('FRANCESA'),
('GRIEGA'),
('HUNGARA'),
('IRLANDESA'),
('ISLANDESA'),
('ITALIANA'),
('LIECHTENSTENSE'),
('LUXEMBURGUESA'),
('MALTESA'),
('MONEGASCA'),
('NORUEGA'),
('HOLANDESA'),
('PORTUGUESA'),
('BRITANICA'),
('SOVIETICA BIELORRUSA'),
('SOVIETICA UCRANIANA'),
('RUMANA'),
('SAN MARINENSE'),
('SUECA'),
('SUIZA'),
('YUGOSLAVA'),
('AUSTRALIANA'),
('FIJIANA'),
('SALOMONESA'),
('NAURUANA'),
('PAPUENSE'),
('SAMOANA'),
('ESLOVACA'),
('BURKINA FASO'),
('ESTONIA'),
('MICRONECIA'),
('REINO UNIDO(DEPEN. TET. BRIT.)'),
('REINO UNIDO(BRIT. DEL EXT.)'),
('REINO UNIDO(C. BRIT. DEL EXT.)'),
('REINO UNIDO'),
('KIRGUISTAN'),
('LITUANIA '),
('MOLDOVIA, REPUBLICA DE'),
('MACEDONIA'),
('ESLOVENIA'),
('ESLOVAQUIA');

ALTER TABLE catalogues_numbertype COLLATE='utf8_general_ci';
INSERT INTO catalogues_numbertype (number_type) VALUES
('Celular'),
('Fijo'),
('Oficina');

ALTER TABLE catalogues_officeslist COLLATE='utf8_general_ci';
INSERT INTO catalogues_officeslist (office_name) VALUES
('Central');

ALTER TABLE catalogues_paymentmethod COLLATE='utf8_general_ci';
INSERT INTO catalogues_paymentmethod (payment_method) VALUES
('Asimilados a salarios'),
('Factura');

ALTER TABLE catalogues_referencerelation COLLATE='utf8_general_ci';
INSERT INTO catalogues_referencerelation (relation) VALUES
('Amigo'),
('Vecino'),
('Familiar'),
('Socio'),
('Otro');

ALTER TABLE catalogues_sexlist COLLATE='utf8_general_ci';
INSERT INTO catalogues_sexlist (sex) VALUES
('Masculino'),
('Femenino'),
('No binario');

ALTER TABLE catalogues_statusimss COLLATE='utf8_general_ci';
INSERT INTO catalogues_statusimss (status_imss) VALUES
('Alta'),
('Baja');

ALTER TABLE catalogues_statusissue COLLATE='utf8_general_ci';
INSERT INTO catalogues_statusissue (status_issue) VALUES
('Sin atender'),
('Resuelto');

ALTER TABLE catalogues_statusreason COLLATE='utf8_general_ci';
INSERT INTO catalogues_statusreason (statusreason) VALUES
('Nuevo'),
('Inpago'),
('Pago'),
('Empleo');

ALTER TABLE catalogues_statusservices COLLATE='utf8_general_ci';
INSERT INTO catalogues_statusservices (status) VALUES
('Activo'),
('Inactivo');

ALTER TABLE catalogues_statususer COLLATE='utf8_general_ci';
INSERT INTO catalogues_statususer (status_user) VALUES
('Alta'),
('Baja'),
('Reingreso'),
('Cancelado');

ALTER TABLE catalogues_usertype COLLATE='utf8_general_ci';
INSERT INTO catalogues_usertype (user_type) VALUES
('Director'),
('Promotor ascendente'),
('Socio');

ALTER TABLE catalogues_status COLLATE='utf8_general_ci';
INSERT INTO catalogues_status (status) VALUES
('Activo'),
('Inactivo');

ALTER TABLE catalogues_videotutorialstatus COLLATE='utf8_general_ci';
INSERT INTO catalogues_videotutorialstatus (status) VALUES
('Activo'),
('Inactivo');

ALTER TABLE catalogues_paymentimss COLLATE='utf8_general_ci';
INSERT INTO catalogues_paymentimss (veces, diario, aport_coop, com_prom, aport_letter) VALUES
(0,148.1,2300,250, 'Dos mil trescientos pesos M. N. 00/100'),
(1,148.1,2300,250, 'Dos mil trescientos pesos M. N. 00/100'),
(1.5,222.15,2700,250, 'Dos mil setecientos pesos M. N. 00/100'),
(2,296.2,3100,250, 'Tres mil cien pesos M. N. 00/100'),
(2.5,370.25,3500,250, 'Tres mil quinientos pesos M. N. 00/100'),
(3,444.3,3925,250, 'Tres mil novecientos veinticinco pesos M. N. 00/100'),
(3.5,518.35,4330,250, 'Cuatro mil trescientos treina pesos M. N. 00/100'),
(4,592.4,4750,250, 'Cuatro mil setecientos cincuenta pesos M. N. 00/100'),
(4.5,666.45,5200,250, 'Cinco mil doscientos pesos M. N. 00/100'),
(5,740.5,5600,250, 'Cinco mil seiscientos pesos M. N. 00/100'),
(5.5,814.55,6000,250, 'Seis mil pesos M. N. 00/100'),
(6,888.6,6450,250, 'Seis mil cuatrocientos cincuenta pesos M. N. 00/100'),
(6.5,962.65,6850,250, 'Seis mil ochocientos cincuenta pesos M. N. 00/100'),
(7,1036.7,7250,250, 'Siete mil doscientos cincuenta pesos M. N. 00/100'),
(7.5,1110.75,7700,250, 'Siete mil setecientos pesos M. N. 00/100'),
(8,1184.8,8100,250, 'Ocho mil cien pesos M. N. 00/100'),
(8.5,1258.85,8500,250, 'Ocho mil quinientos pesos M. N. 00/100'),
(9,1332.9,8950,250, 'Ocho mil novecientos cincuenta pesos M. N. 00/100'),
(9.5,1406.95,9350,250, 'Nueve mil trescientos cincuenta pesos M. N. 00/100'),
(10,1481,9750,250, 'Nueve mil setecientos cincuenta pesos M. N. 00/100');

ALTER TABLE catalogues_placeofbirth COLLATE='utf8_general_ci';
INSERT INTO catalogues_placeofbirth (state_birth) VALUES
('Aguascalientes'),
('Baja California'),
('Baja California Sur'),
('Campeche'),
('Coahuila de Zaragoza'),
('Colima'),
('Chiapas'),
('Chihuahua'),
('Ciudad de México'),
('Durango'),
('Guanajuato'),
('Guerrero'),
('Hidalgo'),
('Jalisco'),
('México'),
('Michoacán de Ocampo'),
('Morelos'),
('Nayarit'),
('Nuevo León'),
('Oaxaca'),
('Puebla'),
('Querétaro'),
('Quintana Roo'),
('San Luis Potosí'),
('Sinaloa'),
('Sonora'),
('Tabasco'),
('Tamaulipas'),
('Tlaxcala'),
('Veracruz de Ignacio de la Llave'),
('Yucatán'),
('Zacatecas')

INSERT INTO catalogues_ceoliststatus (status) VALUES
('Activo'),
('Inactivo');

INSERT INTO catalogues_promotersliststatus (status) VALUES
('Activo'),
('Inactivo');


-- Modelo Identify Information (ass savior)
CREATE TABLE coop_info_identifyinformation (
Id int AUTO_INCREMENT,
user_id int NOT NULL,
created datetime NOT NULL,
user_type_id int NOT NULL,
affiliation_reason_id int,
affiliate_type_id int,
status_user_id int NOT NULL,
status_reason_id int NOT NULL,
offices_list_id int NOT NULL,
ceo_id int NOT NULL,
upstream_promoter_id int NOT NULL,
status_pmnt_sesion_id int,
PRIMARY KEY (Id)
);