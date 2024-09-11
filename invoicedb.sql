--
-- PostgreSQL database dump
--

-- Dumped from database version 14.9 (Ubuntu 14.9-1.pgdg20.04+1)
-- Dumped by pg_dump version 14.0 (Ubuntu 14.0-1.pgdg20.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: client; Type: TABLE; Schema: public; Owner: sysdba
--

CREATE TABLE public.client (
    id bigint NOT NULL,
    name character varying(150) NOT NULL,
    address text NOT NULL,
    email character varying(150) NOT NULL,
    phone character varying(25) NOT NULL,
    post_addr character varying(20) NOT NULL,
    date_created timestamp without time zone NOT NULL
);


ALTER TABLE public.client OWNER TO sysdba;

--
-- Name: client_invoice_id_seq; Type: SEQUENCE; Schema: public; Owner: sysdba
--

CREATE SEQUENCE public.client_invoice_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.client_invoice_id_seq OWNER TO sysdba;

--
-- Name: email_queue; Type: TABLE; Schema: public; Owner: sysdba
--

CREATE TABLE public.email_queue (
    id bigint NOT NULL,
    field character varying(150),
    reference character varying(150),
    date_created timestamp without time zone,
    status integer
);


ALTER TABLE public.email_queue OWNER TO sysdba;

--
-- Name: email_queue_id_seq; Type: SEQUENCE; Schema: public; Owner: sysdba
--

CREATE SEQUENCE public.email_queue_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.email_queue_id_seq OWNER TO sysdba;

--
-- Name: email_receipt_count; Type: TABLE; Schema: public; Owner: sysdba
--

CREATE TABLE public.email_receipt_count (
    id bigint NOT NULL,
    ref character varying(240) NOT NULL,
    counter bigint NOT NULL,
    last_received timestamp without time zone NOT NULL,
    body character varying(240)
);


ALTER TABLE public.email_receipt_count OWNER TO sysdba;

--
-- Name: email_receipt_id_seq; Type: SEQUENCE; Schema: public; Owner: sysdba
--

CREATE SEQUENCE public.email_receipt_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.email_receipt_id_seq OWNER TO sysdba;

--
-- Name: expense; Type: TABLE; Schema: public; Owner: sysdba
--

CREATE TABLE public.expense (
    id bigint NOT NULL,
    title character varying(100),
    "desc" text,
    date_created timestamp without time zone NOT NULL,
    requested_by character varying(100) NOT NULL,
    status integer NOT NULL,
    aproved_by character varying(100) NOT NULL,
    amount numeric(15,2) NOT NULL,
    payment_type integer
);


ALTER TABLE public.expense OWNER TO sysdba;

--
-- Name: expense_id_seq; Type: SEQUENCE; Schema: public; Owner: sysdba
--

CREATE SEQUENCE public.expense_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.expense_id_seq OWNER TO sysdba;

--
-- Name: invoice; Type: TABLE; Schema: public; Owner: sysdba
--

CREATE TABLE public.invoice (
    id bigint NOT NULL,
    disc_type character varying(10),
    disc_value numeric(15,2),
    purchase_no integer,
    invoice_no character varying(30),
    date_value timestamp without time zone,
    invoice_due timestamp without time zone,
    client_type integer NOT NULL,
    currency integer NOT NULL,
    client_id bigint NOT NULL,
    disc_desc text,
    is_dummy integer
);


ALTER TABLE public.invoice OWNER TO sysdba;

--
-- Name: invoice_inv_id_seq; Type: SEQUENCE; Schema: public; Owner: sysdba
--

CREATE SEQUENCE public.invoice_inv_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.invoice_inv_id_seq OWNER TO sysdba;

--
-- Name: item; Type: TABLE; Schema: public; Owner: sysdba
--

CREATE TABLE public.item (
    id bigint NOT NULL,
    item_desc character varying(150) NOT NULL,
    qty integer NOT NULL,
    rate integer NOT NULL,
    amount numeric(15,2),
    invoice_id bigint NOT NULL
);


ALTER TABLE public.item OWNER TO sysdba;

--
-- Name: item_id_seq; Type: SEQUENCE; Schema: public; Owner: sysdba
--

CREATE SEQUENCE public.item_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.item_id_seq OWNER TO sysdba;

--
-- Name: payment; Type: TABLE; Schema: public; Owner: sysdba
--

CREATE TABLE public.payment (
    id bigint NOT NULL,
    client_name character varying(150) NOT NULL,
    payment_desc text,
    date_created timestamp without time zone NOT NULL,
    payment_mode integer NOT NULL,
    amount_paid numeric(15,2),
    balance numeric(15,2),
    invoice_id bigint NOT NULL,
    status integer NOT NULL
);


ALTER TABLE public.payment OWNER TO sysdba;

--
-- Name: payment_id_seq; Type: SEQUENCE; Schema: public; Owner: sysdba
--

CREATE SEQUENCE public.payment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.payment_id_seq OWNER TO sysdba;

--
-- Name: users; Type: TABLE; Schema: public; Owner: sysdba
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    username character varying(150),
    password character varying(150)
);


ALTER TABLE public.users OWNER TO sysdba;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: sysdba
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO sysdba;

--
-- Data for Name: client; Type: TABLE DATA; Schema: public; Owner: sysdba
--

COPY public.client (id, name, address, email, phone, post_addr, date_created) FROM stdin;
1	Credit Switch Ltd	93B Oduduwa Crescent, Ikeja-GRA, Lagos, Nigeria.	accounts@creditswitch.com	08033966796	23401	2019-12-20 11:13:49.83595
2	Oladiran Matthew	57 ZA Williams Street Kfarms estate iju obawole	toyoski@gmail.com	08033780394	23401	2019-12-23 11:55:13.657768
3	Agulanna Josemaria Michael Jidizu	10 Hughes Avenue Alagomeji Yaba Lagos	agulanna.josemaria72@gmail.com	07036821841	23401	2020-01-11 13:20:42.862436
4	Fatogun Alex	dideolu  Estate, Sandfil Bus Stop,Victoria  Island, lagos	diodio2286@gmail.com	09027044365	23401	2020-01-14 21:59:19.551594
5	Mary Olunuga	Ikate, lekki	abimbola.mayree@gmail.com	08131094450	23401	2020-02-25 12:13:02.258415
6	Elegah Joseph	not specified	Josephelegah@yahoo.com	08166872543	23401	2020-03-06 22:18:55.42598
7	Obinaya Chibike	8 bayo osungbuyi street isheri magodo phase 1	chibykesenzy16@gmail.com	08034131748	23401	2020-03-07 14:16:53.645825
8	SPEEDIFY DELIVERY	House 2b block 14 Jubilee estate Ikorodu lagos.	speedifylogistics@gmail.com	4915210455382	23401	2020-03-11 10:05:54.314355
9	Gazzuzz Logistics	41 Obagun Ave, Papa Ajao, Lagos, Nigeria	gazzuzzlogistics@gmail.com	08038119063	23401	2020-03-17 12:18:51.658169
27	Wilson Oghenemudiakevwe Ofiavwe	7B Banjo Street, Tejuosho, Yaba	oghenekevwe_007@yahoo.com	08089445078	23401	2021-04-29 14:31:07.559281
28	Mr Deji Abimbola	Egbeda	contact@mrdeji.com	2347059378218	23401	2021-06-22 09:58:02.057417
11	Uzodinma Jeff	8, ladipo kuku, Allen	jeffrey@ecardex.com	08137898903	23401	2020-04-21 18:20:39.096083
12	Ibrahim Bashir	52 River Niger Street, AMSSCO Estate, Galadimawa Abuja	fari@weissfari.com	2347062374526	23401	2020-04-24 16:04:04.13141
29	Uwannah Peace	lagos	uwannahpeace@gmail.com	2348067330210	23401	2021-07-30 18:23:05.419359
30	Afriglobal medicare	 8 Mobolaji Bank Anthony Way, Opebi 100271, Ikeja	olobank1@gmail.com	090	23401	2021-08-02 19:18:09.667424
31	Chukwuka Paul Chukwuebuka	lekki, chevron drive	chukwuka932@gmail.com	09099649854	23401	2021-08-09 08:35:31.174684
13	Habib	9 amudatu street, county bus stop, ogba	whoishabyb@gmail.com	2347080444916	23401	2020-06-29 15:12:18.698722
14	Bankola Wickliffe	shomolu, palmgrove	bankolewickliffe@gmail.com	2348034898135	23401	2020-07-13 09:36:20.951404
15	LEAPE	8A Reeve Road, Ikoyi, Lagos	humphrey.okorie@hazelconsulting.net	08032006025	23401	2020-07-17 11:50:16.709128
26	Oxford logistics	7, Jehovah Elohim street, Gowon estates Egbeda by Gemade estate gate Lagos	taymey49@gmail.com	08134333471	23401	2021-04-11 09:59:20.513253
24	ECOMMERCE	ecommerce customers	jeffdico@gmail.com	08137898903	23401	2021-03-05 16:16:36.757179
17	Casia Growth Lab	TWOFOUR54, PO BOX: 77804, ABU DHABI, UAE.	okeibunor@gmail.com	971547617206	97101	2020-09-28 15:46:48.789159
19	Konverse Logistics	2 orimoloye Street, Oke-ira, \r\nOgba-ikeja, Lagos	precsgates@gmail.com	08164433092	23401	2020-12-15 14:11:00.996662
20	phummiekush	25, odo ikare street, \r\n2nd Car wash bustop. Gov road, Ikotun	pkushlimited@gmail.com	07037092233	23401	2021-01-25 16:18:33.599939
21	OWOLABI TAIBAT	25 FABUYI STRÊËT OFF TOKUNBO BARUWA IPAJA LAGOS\r\n	owolabitaibat24@gmail.com	2348028664236	23401	2021-01-29 10:30:18.024779
18	Jimoh Ernest	akoka yaba	enessyelvira@gmail.com	08066144912	23401	2020-10-01 17:10:14.849726
22	HODAYAH'S LOGISTICS	24, SURA MOGAJI STREET, OFF COKER ROAD ILUPEJU LAGOS.	hodayahslogistics@gmail.com	2348180532316	23401	2021-03-03 14:02:56.845245
23	Abisola Roland	2, Shoyebo Close, off Doyin Omololu Street, Alapere Ketu	rollancelogistics@gmail.com	08071675266	23401	2021-03-05 10:38:43.798656
25	Premier Stores And Confectionary Ltd	81 Olaniyi Street. Agbulegba	victoria.iyaji@yahoo.com	2348056281963	23401	2021-03-11 19:32:33.636258
48	Ubosi Stanley R	7 Abraham Afolabi Street, Ijaiye Ojokoro by General Bus-stop	stanobum78@gmail.com	08035031538	112106	2023-05-23 13:59:23.572437
32	Adrielle Logistics Services	lagos	enoh3@aol.com	07061547466	23401	2021-11-01 20:24:15.108164
33	AJALA ANTHONY JOACHIN	Unity Plaza, 12 Otigba Street, Computer Village, Ikeja, Nigeria	ajalaanthonycj@yahoo.co.uk	2348094661112	23401	2021-11-12 15:56:13.918598
34	JadeandMary	ikeja	m14limited@gmail.com	08023543340	23401	2022-01-24 15:46:55.950639
49	Uhegbu Emeka	5 odukoya estate micom bustop egbeda	uhegbuemeka@yahoo.com	07036688596	1009	2023-11-22 08:01:51.371527
35	Greenlife Pharmaceuticals	35a, assiociation avenue, obanikoro	edeworalex21@gmail.com	+2347033697404	23401	2022-01-25 12:41:43.643039
10	Mobifin Services Ltd	1291 Akin Adesola Victoria Island	accounts@mobifinng.com	090	23401	2020-04-15 15:44:04.693385
41	Critters Veterinary Centre	8 Josemaria Escriva Street Lekki Lagos	crittersvetcentre@gmail.com	08166252510	23401	2022-10-18 10:53:21.20119
36	Mr. Ayodeji Bidemi Adebayo	lagos, Nigeria	pluglogistics20@gmail.com	0818855323	23401	2022-01-31 12:20:24.833768
37	AC harmony Ltd	Plot 51 milestone avenue, Ijesha,opp MRS filling station, Onitcha	nonso@acharmony.com	08023787860	23401	2022-03-13 22:29:29.20485
38	sargas energy limited	Wande Alamu Street, MTR Road, Opic	ikechukwu@sargascylinder.com	2348029716876	23401	2022-03-16 18:40:43.556106
39	Hoowfar App	*	info2vicman@gmail.com	447760612291	23401	2022-03-21 15:26:22.585945
42	Kumar medewar	Plot 10 ikosi road oregun ikeja lagos	pramod@coralentnigltd.com	08073355459	23401	2022-11-22 08:26:51.272343
16	ONE PLUG VENTURES	27, Ondo Street by Cemetery road, Ebutemetta, Lagos	pluglogistics20@gmail.com	08081089553	23401	2020-08-11 10:57:21.525701
50	Michael Emerue	1, Marian Road, Prayer Estate; Amuwo Odofin, Lagos	mcemerue@icloud.com	08036225434	23401	2023-12-12 11:12:15.570639
40	Nexus Alliance Ltd	289b Corporation Drive, Dolphin Estate, Ikoyi	samuel@nexusallianceltd.com	08132755827	234	2022-05-13 15:03:53.96739
43	Jkjlogistics	arena shopping complex bolade oshodi	abamtom@gmail.com	07065043828	23401	2023-01-26 11:41:27.997929
44	Uloaku Lovelyn Ajari	lagos	uloakulovelyn@gmail.com	08066178197	23401	2023-03-25 23:08:22.518537
46	Maptrackapp	office address	support@ecardex.com	234813057	23401	2023-03-31 12:32:50.108429
47	WheelsFix Technologies Limited	7, Adekoya Street, Itire, Surulere, Lagos.	zillionaireboss1@yahoo.com	07017328976	101283	2023-05-20 20:25:21.351679
51	Bolatito Ayodele	abuja	oyinbee12@gmail.com	08032319147	23401	2023-12-14 14:50:51.280754
45	Zillionaire Media Global Services Limited	7, Adekoya Street, Itire, Surulere, Lagos	zillionaireboss1@yahoo.com	07017328976	23401	2023-03-31 09:53:53.583932
52	Dike John Uchechukwu	No 10 Akinbaruwa Street, Surulere, Lagos	Kvngxjohn@gmail.com	07033850000	23481	2024-03-07 08:41:24.476714
53	Stevie	Dominion City Ikeja . 75 kudirat Abiola way , opposite conoil , ikeja	steviechrystal048@gmail.com	07036219203	23401	2024-03-22 13:33:09.687731
54	Nigeria Network of NGOs	ibadan	oyindamola.aramide@nnngo.org	07065160956	200005	2024-05-07 15:17:03.050988
55	Ralds and Agate Limited	12 Landbridge Avenue, Oniru Estate, Victoria Island, Lagos, Nigeria	jeffdico@gmail.com	2349037542149	101003	2024-07-05 12:19:45.937633
\.


--
-- Data for Name: email_queue; Type: TABLE DATA; Schema: public; Owner: sysdba
--

COPY public.email_queue (id, field, reference, date_created, status) FROM stdin;
\.


--
-- Data for Name: email_receipt_count; Type: TABLE DATA; Schema: public; Owner: sysdba
--

COPY public.email_receipt_count (id, ref, counter, last_received, body) FROM stdin;
2	ZW1haWxfcmVjZWl2ZXI9amVmZmRpY28lNDBnbWFpbC5jb20mZW1haWxfdGl0bGU9UmVjZWlwdCtHZW5lcmF0ZWQrZm9yK0VDT01NRVJDRQ==	1	2023-03-16 11:34:39.642761	{"email_receiver": "jeffdico@gmail.com", "email_title": "Receipt+Generated+for+ECOMMERCE"}
1	ZW1haWxfcmVjZWl2ZXI9amVmZmRpY28lNDBnbWFpbC5jb20mZW1haWxfdGl0bGU9SW52b2ljZStHZW5lcmF0ZWQrZm9yK0VDT01NRVJDRQ==	3	2023-03-16 20:45:05.064153	{"email_receiver": "jeffdico@gmail.com", "email_title": "Invoice+Generated+for+ECOMMERCE"}
20	ZW1haWxfcmVjZWl2ZXI9YWphbGFhbnRob255Y2olNDB5YWhvby5jby51ayZlbWFpbF90aXRsZT1JbnZvaWNlK0dlbmVyYXRlZCtmb3IrQUpBTEErQU5USE9OWStKT0FDSElO	4	2024-05-17 13:12:37.435058	{"email_receiver": "ajalaanthonycj@yahoo.co.uk", "email_title": "Invoice+Generated+for+AJALA+ANTHONY+JOACHIN"}
4	ZW1haWxfcmVjZWl2ZXI9emlsbGlvbmFpcmVib3NzMSU0MHlhaG9vLmNvbSZlbWFpbF90aXRsZT1JbnZvaWNlK0dlbmVyYXRlZCtmb3IrWklMTElPTkFJUkUrTUVESUErR0xPQkFMK1NFUlZJQ0VTK0xJTUlURUQ=	2	2023-03-31 19:13:31.718378	{"email_receiver": "zillionaireboss1@yahoo.com", "email_title": "Invoice+Generated+for+ZILLIONAIRE+MEDIA+GLOBAL+SERVICES+LIMITED"}
15	ZW1haWxfcmVjZWl2ZXI9dWhlZ2J1ZW1la2ElNDB5YWhvby5jb20mZW1haWxfdGl0bGU9UmVjZWlwdCtHZW5lcmF0ZWQrZm9yK1VIRUdCVStFTUVLQQ==	2	2023-11-23 12:02:58.84887	{"email_receiver": "uhegbuemeka@yahoo.com", "email_title": "Receipt+Generated+for+UHEGBU+EMEKA"}
10	ZW1haWxfcmVjZWl2ZXI9c3Rhbm9idW03OCU0MGdtYWlsLmNvbSZlbWFpbF90aXRsZT1JbnZvaWNlK0dlbmVyYXRlZCtmb3IrVUJPU0krU1RBTkxFWStS	4	2023-07-12 11:49:15.13184	{"email_receiver": "stanobum78@gmail.com", "email_title": "Invoice+Generated+for+UBOSI+STANLEY+R"}
9	ZW1haWxfcmVjZWl2ZXI9c3Rhbm9idW03OCU0MGdtYWlsLmNvbSZlbWFpbF90aXRsZT1SZWNlaXB0K0dlbmVyYXRlZCtmb3IrVUJPU0krU1RBTkxFWStS	4	2023-07-12 12:26:39.964564	{"email_receiver": "stanobum78@gmail.com", "email_title": "Receipt+Generated+for+UBOSI+STANLEY+R"}
6	ZW1haWxfcmVjZWl2ZXI9d2hlZWxzZml4dGVjaGx0ZCU0MGdtYWlsLmNvbSZlbWFpbF90aXRsZT1JbnZvaWNlK0dlbmVyYXRlZCtmb3IrWklMTElPTkFJUkUrTUVESUErR0xPQkFMK1NFUlZJQ0VTK0xJTUlURUQ=	5	2023-05-20 19:55:13.314832	{"email_receiver": "wheelsfixtechltd@gmail.com", "email_title": "Invoice+Generated+for+ZILLIONAIRE+MEDIA+GLOBAL+SERVICES+LIMITED"}
25	ZW1haWxfcmVjZWl2ZXI9b3lpbmRhbW9sYS5hcmFtaWRlJTQwbm5uZ28ub3JnJmVtYWlsX3RpdGxlPUludm9pY2UrR2VuZXJhdGVkK2ZvcitOSUdFUklBK05FVFdPUksrT0YrTkdPUw==	20	2024-08-12 15:45:49.969424	{"email_receiver": "oyindamola.aramide@nnngo.org", "email_title": "Invoice+Generated+for+NIGERIA+NETWORK+OF+NGOS"}
8	ZW1haWxfcmVjZWl2ZXI9d2hlZWxzZml4dGVjaGx0ZCU0MGdtYWlsLmNvbSZlbWFpbF90aXRsZT1SZWNlaXB0K0dlbmVyYXRlZCtmb3IrV0hFRUxTRklYK1RFQ0hOT0xPR0lFUytMSU1JVEVE	1	2023-05-20 20:47:20.886865	{"email_receiver": "wheelsfixtechltd@gmail.com", "email_title": "Receipt+Generated+for+WHEELSFIX+TECHNOLOGIES+LIMITED"}
7	ZW1haWxfcmVjZWl2ZXI9d2hlZWxzZml4dGVjaGx0ZCU0MGdtYWlsLmNvbSZlbWFpbF90aXRsZT1JbnZvaWNlK0dlbmVyYXRlZCtmb3IrV0hFRUxTRklYK1RFQ0hOT0xPR0lFUytMSU1JVEVE	2	2023-05-20 20:47:21.50663	{"email_receiver": "wheelsfixtechltd@gmail.com", "email_title": "Invoice+Generated+for+WHEELSFIX+TECHNOLOGIES+LIMITED"}
11	ZW1haWxfcmVjZWl2ZXI9bTE0bGltaXRlZCU0MGdtYWlsLmNvbSZlbWFpbF90aXRsZT1SZWNlaXB0K0dlbmVyYXRlZCtmb3IrSkFERUFORE1BUlk=	7	2024-05-23 10:37:27.662903	{"email_receiver": "m14limited@gmail.com", "email_title": "Receipt+Generated+for+JADEANDMARY"}
14	ZW1haWxfcmVjZWl2ZXI9dWhlZ2J1ZW1la2ElNDB5YWhvby5jb20mZW1haWxfdGl0bGU9SW52b2ljZStHZW5lcmF0ZWQrZm9yK1VIRUdCVStFTUVLQQ==	1	2023-11-22 09:30:02.14653	{"email_receiver": "uhegbuemeka@yahoo.com", "email_title": "Invoice+Generated+for+UHEGBU+EMEKA"}
3	ZW1haWxfcmVjZWl2ZXI9bTE0bGltaXRlZCU0MGdtYWlsLmNvbSZlbWFpbF90aXRsZT1JbnZvaWNlK0dlbmVyYXRlZCtmb3IrSkFERUFORE1BUlk=	21	2024-08-21 15:48:53.545541	{"email_receiver": "m14limited@gmail.com", "email_title": "Invoice+Generated+for+JADEANDMARY"}
23	ZW1haWxfcmVjZWl2ZXI9c3RldmllY2hyeXN0YWwwNDglNDBnbWFpbC5jb20mZW1haWxfdGl0bGU9SW52b2ljZStHZW5lcmF0ZWQrZm9yK1NURVZJRQ==	1	2024-03-22 13:34:06.362728	{"email_receiver": "steviechrystal048@gmail.com", "email_title": "Invoice+Generated+for+STEVIE"}
17	ZW1haWxfcmVjZWl2ZXI9bWNlbWVydWUlNDBpY2xvdWQuY29tJmVtYWlsX3RpdGxlPVJlY2VpcHQrR2VuZXJhdGVkK2ZvcitNSUNIQUVMK0VNRVJVRQ==	3	2023-12-18 21:01:28.031992	{"email_receiver": "mcemerue@icloud.com", "email_title": "Receipt+Generated+for+MICHAEL+EMERUE"}
16	ZW1haWxfcmVjZWl2ZXI9bWNlbWVydWUlNDBpY2xvdWQuY29tJmVtYWlsX3RpdGxlPUludm9pY2UrR2VuZXJhdGVkK2ZvcitNSUNIQUVMK0VNRVJVRQ==	3	2023-12-18 21:02:38.88239	{"email_receiver": "mcemerue@icloud.com", "email_title": "Invoice+Generated+for+MICHAEL+EMERUE"}
18	ZW1haWxfcmVjZWl2ZXI9b3lpbmJlZTEyJTQwZ21haWwuY29tJmVtYWlsX3RpdGxlPUludm9pY2UrR2VuZXJhdGVkK2ZvcitCT0xBVElUTytBWU9ERUxF	3	2023-12-26 14:07:06.688667	{"email_receiver": "oyinbee12@gmail.com", "email_title": "Invoice+Generated+for+BOLATITO+AYODELE"}
5	ZW1haWxfcmVjZWl2ZXI9d2hlZWxzZml4dGVjaGx0ZCU0MGdtYWlsLmNvbSZlbWFpbF90aXRsZT1SZWNlaXB0K0dlbmVyYXRlZCtmb3IrWklMTElPTkFJUkUrTUVESUErR0xPQkFMK1NFUlZJQ0VTK0xJTUlURUQ=	23	2024-01-11 05:53:30.029143	{"email_receiver": "wheelsfixtechltd@gmail.com", "email_title": "Receipt+Generated+for+ZILLIONAIRE+MEDIA+GLOBAL+SERVICES+LIMITED"}
19	ZW1haWxfcmVjZWl2ZXI9emlsbGlvbmFpcmVib3NzMSU0MHlhaG9vLmNvbSZlbWFpbF90aXRsZT1JbnZvaWNlK0dlbmVyYXRlZCtmb3IrV0hFRUxTRklYK1RFQ0hOT0xPR0lFUytMSU1JVEVE	1	2024-01-16 04:21:51.776729	{"email_receiver": "zillionaireboss1@yahoo.com", "email_title": "Invoice+Generated+for+WHEELSFIX+TECHNOLOGIES+LIMITED"}
21	ZW1haWxfcmVjZWl2ZXI9S3ZuZ3hqb2huJTQwZ21haWwuY29tJmVtYWlsX3RpdGxlPUludm9pY2UrR2VuZXJhdGVkK2ZvcitESUtFK0pPSE4rVUNIRUNIVUtXVQ==	3	2024-03-07 13:58:14.428846	{"email_receiver": "Kvngxjohn@gmail.com", "email_title": "Invoice+Generated+for+DIKE+JOHN+UCHECHUKWU"}
22	ZW1haWxfcmVjZWl2ZXI9S3ZuZ3hqb2huJTQwZ21haWwuY29tJmVtYWlsX3RpdGxlPVJlY2VpcHQrR2VuZXJhdGVkK2ZvcitESUtFK0pPSE4rVUNIRUNIVUtXVQ==	3	2024-03-07 13:58:14.783508	{"email_receiver": "Kvngxjohn@gmail.com", "email_title": "Receipt+Generated+for+DIKE+JOHN+UCHECHUKWU"}
12	ZW1haWxfcmVjZWl2ZXI9YWNjb3VudHMlNDBtb2JpZmlubmcuY29tJmVtYWlsX3RpdGxlPUludm9pY2UrR2VuZXJhdGVkK2ZvcitNT0JJRklOK1NFUlZJQ0VTK0xURA==	65	2024-05-23 17:34:32.970274	{"email_receiver": "accounts@mobifinng.com", "email_title": "Invoice+Generated+for+MOBIFIN+SERVICES+LTD"}
13	ZW1haWxfcmVjZWl2ZXI9YWNjb3VudHMlNDBtb2JpZmlubmcuY29tJmVtYWlsX3RpdGxlPVJlY2VpcHQrR2VuZXJhdGVkK2ZvcitNT0JJRklOK1NFUlZJQ0VTK0xURA==	6	2024-05-17 11:03:05.410572	{"email_receiver": "accounts@mobifinng.com", "email_title": "Receipt+Generated+for+MOBIFIN+SERVICES+LTD"}
24	ZW1haWxfcmVjZWl2ZXI9b3lpbmRhbW9sYS5hcmFtaWRlJTQwbm5uZ28ub3JnJmVtYWlsX3RpdGxlPVJlY2VpcHQrR2VuZXJhdGVkK2ZvcitOSUdFUklBK05FVFdPUksrT0YrTkdPUw==	11	2024-08-15 14:01:07.838715	{"email_receiver": "oyindamola.aramide@nnngo.org", "email_title": "Receipt+Generated+for+NIGERIA+NETWORK+OF+NGOS"}
26	ZW1haWxfcmVjZWl2ZXI9amVmZmRpY28lNDBnbWFpbC5jb20mZW1haWxfdGl0bGU9SW52b2ljZStHZW5lcmF0ZWQrZm9yK1JBTERTK0FORCtBR0FURStMSU1JVEVE	11	2024-07-05 22:04:07.290742	{"email_receiver": "jeffdico@gmail.com", "email_title": "Invoice+Generated+for+RALDS+AND+AGATE+LIMITED"}
\.


--
-- Data for Name: expense; Type: TABLE DATA; Schema: public; Owner: sysdba
--

COPY public.expense (id, title, "desc", date_created, requested_by, status, aproved_by, amount, payment_type) FROM stdin;
1	Facebook ad campaign	Facebook ad campaign for Jan and Feb campaign	2019-12-20 11:04:15.873179	Jeffrey	2	Jeffrey	20000.00	\N
39	Vat Remittance Jan	Vat Remittance Jan	2020-02-11 18:48:16.069403	Jeffrey	2	Jeffrey	11500.00	5
40	Linux Server Cost	Server for maptrackapp product operations	2020-02-11 19:01:58.259613	Jeffrey	2	Jeffrey	33000.00	1
10	Car Tracker Installation	Paid an electricitian to install one of the trackers on the vehicle for experimental purposes	2020-01-06 15:06:38.677168	Jeffrey	2	Jeffrey	3000.00	\N
12	Soft loan	From jeffrey's personal account	2020-01-07 12:34:11.384947	Jeffrey	2	Jeffrey	20000.00	\N
13	Fuel Purchase Loan	Soft loan to the business	2020-01-07 12:34:53.86712	jeffrey	2	Jeffrey	10000.00	\N
14	Office Beverages	Beverages for office consumption	2020-01-09 15:12:53.29402	Jeffrey	2	Jeffrey	4200.00	\N
19	Office Payout	Payment for service UI Mockup -- Samson Ilorin	2020-01-15 09:16:21.414026	Jeffrey	2	Jeffrey	20000.00	\N
20	Office Payout	Dev Assistance -- For Application	2020-01-15 09:18:03.248008	Jeffrey	2	Jeffrey	32000.00	\N
23	GPS Devices	Purchase for GPS devices	2020-01-15 09:22:58.281588	Jeffrey	2	Jeffrey	66000.00	\N
41	Fuel	office fuel for operations	2020-02-13 17:59:23.426982	Jeffrey	2	Jeffrey	3000.00	1
42	Office Utility	Office Utility	2020-02-13 17:59:54.426829	Jeffrey	2	Jeffrey	4000.00	1
27	Office utility purchases	Office Utility Purchases	2020-01-26 12:20:02.592138	Jeffrey	2	Jeffrey	2600.00	1
26	AC Compressor repair	AC Compressor repair	2020-01-25 13:10:03.374672	Jeffrey	2	Jeffrey	15000.00	1
25	Internet Sub	Office Internet sub  for feb	2020-01-22 08:21:44.686606	Jeffrey	2	Jeffrey	11200.00	1
24	Payout	Data science instructor Payout	2020-01-20 08:32:11.479388	Jeffrey	2	Jeffrey	60000.00	4
22	Office Utility fee 	Payment for office utility service	2020-01-15 09:19:39.435526	Jeffrey	2	Jeffrey	72000.00	1
21	Paint Job	Payment for a painting serrvice	2020-01-15 09:19:00.879568	Jeffrey	2	Jeffrey	40000.00	4
18	Office Utility	Power and Water purchase	2020-01-15 09:08:42.229635	Jeffrey	2	Jeffrey	4000.00	1
17	Domain Purchase	Maptrackapp.com  domain purchase	2020-01-13 14:21:54.823225	Jeffrey	2	Jeffrey	4000.00	1
16	Office Training Material	Coffee cups for students	2020-01-13 14:20:44.817207	Jeffrey	2	Jeffrey	2000.00	1
15	Office Electrical Circuits	Office Electrical Circuits	2020-01-10 11:06:19.153918	Jeffrey	2	Jeffrey	5000.00	1
11	Soft Loan	Small loan gotten for dec upkeep	2020-01-06 19:23:58.138003	Jeffrey	2	Jeffrey	18000.00	4
8	Drawings	Personal expenditure	2020-01-04 16:21:42.20805	Jeffrey	2	Jeffrey	10000.00	4
6	Facebook ads 	Ads fee payment for Dec 2019 ads campaign 	2020-01-03 09:40:09.737067	Jeffrey	2	Jeffrey	17000.00	1
4	Internet Sub	Sub for January Internet	2019-12-24 08:40:44.632036	Jeffrey	2	Jeffrey	11200.00	1
5	Drawings	Personal expenditure	2020-01-01 16:31:26.104805	Jeffrey	2	Jeffrey	20000.00	4
3	Car Repair	Car repair and fixing	2019-12-23 15:58:45.204049	Jeffrey	2	Jeffrye	5000.00	1
2	Miscelleneous expenditures	All frequent expenses that arises from time to time	2019-12-20 12:16:20.429261	Jeffrey	2	Jeffrey	20000.00	4
7	Twilo sms units	Twilo sms units for mapapp sms vending 	2020-01-04 04:02:06.081846	Jeffrey	2	Jeffrey	7500.00	1
28	Laptop stand	exerrnal laptop stand	2020-01-26 14:29:37.391085	Jeffrey	2	Jeffrey	12000.00	1
29	office Fuel	Fuel for gen and movements	2020-01-28 10:29:37.459036	Jeffrey	2	Jeffrey	10000.00	1
30	AC repairs balance	AC repairs balance	2020-01-28 13:50:04.154577	Jeffrey	2	Jeffrey	2000.00	1
31	FB ads Payment 	Payment for Jan ads campaign	2020-01-30 08:37:08.979093	Jeffrey	2	Jeffrey	6000.00	1
32	Salary Payout -- Esther 	Salary payout For Esther	2020-01-30 08:38:05.291937	Jeffrey	2	Jeffrey	10000.00	2
33	Cleaning Service	Tips for cleaning service	2020-01-30 08:38:45.341532	Jeffrey	2	Jeffrey	3000.00	1
34	drawings	Drawing for miscellaneous 	2020-02-01 11:15:55.429637	Jeffrey	2	Jeffrey	40000.00	4
35	Office Mobile Phone	Office Mobile Phone	2020-02-03 23:07:29.897757	Jeffrey	2	Jeffrey	17000.00	1
36	Car repair	Car repairs	2020-02-08 23:58:57.000409	Jeffrey	2	Jeffrey	20000.00	1
37	Complementary Card	Complementary Card	2020-02-11 18:43:08.943858	Jeffrey	2	Jeffrey	3500.00	1
38	Vat Account Fee	Vat Account Fee	2020-02-11 18:43:41.46794	Jeffrey	2	Jeffrey	10000.00	5
43	Electricity Bill Payment	Electricity Bill payment	2020-02-13 19:10:23.04691	Jeffrey	2	Jeffrey	2000.00	1
44	Car Repair	Car Repair	2020-02-19 19:37:04.162717	Jeffrey	2	Jeffrey	8000.00	4
45	Drawings	Drawings	2020-02-19 19:37:31.180344	Jeffrey	2	Jeffrey	20000.00	4
9	Loan Repayment	soft loan repaid to chioma	2020-01-04 16:22:29.30136	Jeffrey	2	Jeffrey	25000.00	4
46	Drawings	Drawings	2020-02-23 21:58:49.314574	Jeffrey	2	Jeffrey	20000.00	4
47	Internet Sub	Internet sub for march	2020-02-23 22:00:57.475632	Jeffrey	2	Jeffrey	11500.00	1
48	Maptrack SMS Unit	Maptrack SMS Units	2020-02-25 14:55:55.250675	Jeffrey	2	Jeffrey	2030.00	1
49	Staff Salary 	Staff Salary for Victoria Bolten	2020-02-27 13:44:20.155656	Jeffrey	2	Jeffrey	20000.00	2
50	Bonus Payout	Bonus Payout For Staff performance	2020-02-27 13:45:22.786752	Jeffrey	2	Jeffrey	5000.00	3
51	Drawings	Drawings for exp	2020-02-29 12:18:50.473535	Jeffrey	2	Jeffrey	20000.00	4
52	Gps Devices	Purchases of GPS devices	2020-03-02 19:37:33.152468	Jeffrey	2	Jeffrey	15000.00	1
53	GPS Device Purchase Loan	Additional loan to purchase gps devices	2020-03-02 19:38:30.457098	jeffrey	2	Jeffrey	200000.00	1
54	Fuel	Fuel for operatons	2020-03-04 08:26:49.52041	Jeffrey	2	Jeffrey	10000.00	1
55	expenses	expenses	2020-03-05 11:13:08.544604	Jeffrey	2	Jeffrey	10000.00	1
56	installation exp	tracker installation exp	2020-03-07 18:10:15.914884	jeffrey	2	Jeffrey	10000.00	1
57	vat payout feb	vat payout for feb	2020-03-09 10:07:39.672432	Jeffrey	2	Jeffrey	2025.00	5
58	Electricity bill	Electricity bill	2020-03-10 08:51:44.636059	Jeffrey	2	Jeffrey	2000.00	1
59	drawings	Drawings for expediture	2020-03-10 08:52:28.413426	Jeffrey	2	Jeffrey	12000.00	4
60	Facebook Ads Feb	Facebook Ads Feb Payment	2020-03-12 23:36:00.891556	Jeffrey	2	Jeffrey	20000.00	1
61	Fuel Purchase	Fuel purchase	2020-03-13 11:12:19.691935	Jeffrey	2	Jeffrey	10000.00	1
62	Datascience nstructor Payout	Datascience  Instructor Payout	2020-03-16 16:23:04.386781	David Abu	2	Jeffrey	40000.00	2
63	Drawings	mapapp installation setup issues rectification	2020-03-16 16:25:21.75093	Jeffrey	2	Jeffrey	17000.00	4
65	Tracker Device haulage -Jan	Tracker device haulage fees for Jan batch	2020-03-16 19:18:02.698988	Jeffrey	2	Jeffrey	5791.00	1
64	Tracker Device haulage - March	Tracker Devices Import Fees from china	2020-03-16 19:11:44.863831	Jeffrey	2	Jeffrey	17475.00	1
66	drawings	expenditures	2020-03-19 08:44:39.823142	Jeffrey	2	Jeffrey	10000.00	4
67	Drawings	Drawings for expenditures	2020-03-23 09:08:31.518076	Jeffrey	2	Jeffrey	13000.00	4
68	INV-5 Account Refund	Maptrackapp customer device purchase refund.	2020-03-24 11:52:09.787646	Mary Olunuga	2	Jeffrey	13975.00	1
69	Internet sub -April	Internet sub for April	2020-03-25 18:45:50.847858	jeffrey	2	Jeffrey	11550.00	1
70	Drawings	Drawings for expenditures	2020-03-25 18:47:35.042377	Jeffrey	2	Jeffrey	15000.00	4
71	EXP	for upwork jobsearch	2020-03-27 11:37:34.52955	Jeffrey	2	Jeffrey	10000.00	1
72	Staff Salary	Staff salary for march	2020-03-31 10:29:49.483994	Victoria	2	Jeffrey	20000.00	2
73	Staff Salary	Staff Salary for March	2020-03-31 10:30:37.098882	Viictor	2	Jeffrey	40000.00	2
74	Drawing	Drawings for expenses	2020-04-01 16:02:21.591149	Jeffrey	2	Jeffrey	15000.00	1
75	Drawings	Drawings for utilities and expenditures	2020-04-02 12:55:20.194389	Jeffrey	2	Jeffrey	5000.00	1
76	Expenses	Expenses	2020-04-09 09:40:47.153499	Jeffrey	2	Jeffrey	12000.00	1
77	Power Units	Electricity Power unit	2020-04-10 12:01:31.328656	Jeffrey	2	Jeffrey	2000.00	1
78	Internet sub 	Internet sub	2020-04-21 11:12:51.312408	Jeffrey	2	Jeffrey	11500.00	1
79	Office exp	Office exp	2020-04-21 11:13:33.559927	Jeffrey	2	Jeffrey	5000.00	1
80	office exp	office exp	2020-04-24 11:46:13.910351	Jeffrey	2	Jeffrey	10000.00	1
81	Gen repairs	Gen servicing and repairs	2020-04-27 12:56:04.405202	Jeffrey	2	Jeffrey	2800.00	1
82	Office Exp	Office exp	2020-04-29 11:52:04.529365	Jeffrey	2	Jeffrey	10000.00	1
83	Dammilola	Book keep fee	2020-05-02 12:20:59.466107	Jeffrey	2	Jeffrey	30000.00	1
84	drinking water	Drinking water purchase	2020-05-02 12:21:43.887725	Jeffrey	2	Jeffrey	1200.00	1
85	Office exp	office exp	2020-05-05 13:57:23.617674	Jeffrey	2	Jeffrey	10000.00	1
86	laptop battery	official laptop battery relacement	2020-05-06 10:23:58.70821	Jeffrey	2	Jeffrey	5000.00	1
87	Office exp	office electricity exp	2020-05-07 13:03:25.690375	Jeffrey	2	Jeffrey	2400.00	1
88	Expenses	Expenses and laptop repairs	2020-05-13 11:07:47.565314	Jeffrey	2	Jeffrey	30000.00	1
89	Car repairs	Car repairs	2020-05-13 17:09:16.388223	jeffrey	2	Jeffrey	10000.00	1
90	expenses	for office expenses	2020-05-17 13:25:30.694865	jeffrey	2	Jeffrey	10000.00	1
91	Offfice Expenses 	Office expenses plus internet	2020-05-19 21:31:01.670457	Jeffrey	2	Jeffrey	20000.00	1
92	office expenses	office expenses	2020-05-23 13:31:57.947519	jeffrey	2	Jeffrey	10000.00	1
93	glass frame	payment for glass frame and glass lense	2020-05-27 10:25:08.303833	jeffrey	2	Jeffrey	13500.00	4
94	charge controller	charge controller for solar power setup. useful to guarantee operations. 	2020-05-27 10:26:12.603011	jeffrey	2	Jeffrey	9000.00	1
95	office expense	drinking water and electrical power purchase	2020-05-28 09:06:51.877594	Jeffrey	2	Jeffrey	3200.00	1
96	Payout	for Project participation	2020-05-28 09:07:42.685154	Jeffrey	2	Jeffrey	35000.00	2
97	drawing	made dawings	2020-05-29 14:15:37.344385	jeffrey	2	Jeffrey	10000.00	4
99	expenses	purchase of fan and fuel	2020-06-01 16:20:45.933432	Jeffrey	2	Jeffrey	15000.00	1
100	laptop repairs 	laptop repairs and electric fan fixes	2020-06-03 13:48:56.432783	Jeffrey	2	Jeffrey	12000.00	1
101	Drawings	For personal expenses	2020-06-04 10:33:09.810192	Jeffrey	2	Jeffrey	10000.00	4
102	expense	office expenses 	2020-06-05 13:23:52.276117	Jeff	2	Jeff	10000.00	1
103	Expenses	general expenses	2020-06-09 13:08:54.26853	Jeff	2	Jeff	10000.00	1
104	expenses	expenses	2020-06-12 16:22:21.63047	Jeffrey	2	Jeffrey	10000.00	1
105	Expense	Standing table desk for working	2020-06-13 10:35:05.541778	Jeff	2	Jeff	12000.00	1
106	Office Expense	Internet subscription	2020-06-14 12:06:53.878939	jeff	2	Jeff	11550.00	1
127	Vat Remmitance	Vat Remittance for July -- Habib	2020-08-04 11:11:01.422129	Jeff	2	Jeff	3375.00	5
107	facebook ads exp	facebook ads expenditure and office exp	2020-06-17 23:12:11.002867	Jeff	2	Jeff	18000.00	1
108	expenses	office exp, ikeja electric, and keyboard purchase	2020-06-19 13:22:32.588473	Jeff	2	Jeff	10000.00	1
109	car repairs	car part replacement and ac fixes	2020-06-26 11:47:10.465012	jeff	2	Jeffrey	73000.00	4
110	Tracker Installation	Tracker Installation fee	2020-07-01 17:37:42.440292	Jeff	2	Jeff	5000.00	1
111	Payout	bonus payout	2020-07-02 17:05:57.708067	Jeff	2	Jeff	25000.00	3
112	office exp	expenditures for office operations	2020-07-02 17:07:01.223784	Jeff	2	Jeff	14000.00	1
113	office printer	office printer purchase	2020-07-03 12:03:21.269432	Victor	2	Jeff	18500.00	1
114	expenses	office expenses	2020-07-06 16:20:36.577349	Jeff	2	Jeff	10000.00	1
115	expenses	office expenses	2020-07-08 16:34:01.863724	Jeff	2	Jeff	10000.00	1
116	Office Internet	Office internet subscription	2020-07-10 00:15:46.469096	Jeff	2	Jeff	11500.00	1
117	cargo cost	shiping from china cost	2020-07-14 19:25:34.368953	Jeff	2	Jeff	6628.00	1
118	expense	daily operational exp	2020-07-16 16:10:45.520501	Jeff	2	Jeff	10000.00	1
119	office chair	office chair purchase for back pain relief	2020-07-23 15:01:13.092461	Jeff	2	Jeff	60000.00	1
120	office exp	office expenditures	2020-07-24 10:26:57.626454	Jeff	2	Jeff	10000.00	1
121	office internet	office internet subscription	2020-07-25 10:14:10.523164	Jeff	2	Jeff	12000.00	1
122	drawings	drawings for the personal expeses	2020-07-26 14:22:30.877526	Jeff	2	Jeff	10000.00	1
125	expenses 	office expenses	2020-08-01 09:39:12.237368	Jeff	2	Jeff	10000.00	1
124	office exp	office exp and utility bill payments	2020-07-31 09:11:35.446429	Jeff	2	Jeff	10000.00	1
123	office exp	office expenses	2020-07-30 12:46:48.609181	Jeff	2	Jeff	10000.00	1
126	Cloud Server Payment	Cloud Server Payment for the month of July	2020-08-02 14:11:37.922107	Jeff	2	Jeff	10500.00	1
128	Vat Remmitance 	Vattance Remmitance for July -- Bankole Wickliff	2020-08-04 11:11:53.053683	Jeff	2	Jeff	2100.00	5
98	vat remmitance	vat remmitance for may on remmita	2020-06-01 09:50:04.066287	Jeffrey	2	Jeffrey	14640.00	5
129	Vat Remmitance	Vat Remittance For July -- Weisfari	2020-08-04 11:13:45.314962	Jeff	2	Jeff	11250.00	5
130	Vat Remittance	Vat Remittance for Mobifin - on 50% first payment	2020-08-04 11:15:04.424087	Jeff	2	Jeff	19650.00	5
132	drawing	drawing for personal exp	2020-08-04 12:24:30.26973	Jeff	2	Jeff	10000.00	1
131	Rents Payment	Rents payment	2020-08-04 12:23:43.411419	Jeff	2	Jeff	550000.00	1
133	drawings	drawings for personal use	2020-08-05 16:08:26.503031	Jeff	2	Jeff	150000.00	1
640	opex	internet sub	2024-08-10 19:36:39.372712	Jeff	2	Jeff	11000.00	1
134	laptop purchase	Laptop purchase for office activity	2020-08-07 05:26:12.937596	Jeff	2	Jeff	50000.00	1
135	Laptop keyboard repair	laptop keyboard repair	2020-08-07 05:27:34.006253	Jeff	2	Jeff	5000.00	1
136	Office expenses	office expenses	2020-08-07 05:33:15.380243	Jeff	2	Jeff	50000.00	1
137	office exp	office exp for daily operations	2020-08-09 10:50:17.727263	Jeff	2	Jeff	30000.00	1
138	exp	office exp	2020-08-10 19:30:02.183781	Jeff	2	Jeff	10000.00	1
139	Payout	For project participation in mobifin api integration	2020-08-12 18:15:36.660819	Victor Akpokiro	2	Jeff	30000.00	3
140	exp	office expenses	2020-08-13 16:06:55.774357	Jeff	2	Jeff	10000.00	1
142	exp	fuel for operations 	2020-08-14 12:35:40.93882	Jeff	2	Jeff	5000.00	1
143	Tracker Installation Fee	Payment for tracker installations	2020-08-16 18:33:44.855207	Obinna	2	Jeff	5000.00	1
144	Car licences renewal	Car license renewal fee	2020-08-17 13:11:21.63872	Jeff	2	Jeff	15000.00	1
145	internet sub	internet subscription renewal fee	2020-08-19 10:31:05.477178	Jeff	2	Jeff	12000.00	1
146	expenses	expenses for office operations	2020-08-19 10:31:50.633112	Jeff	2	Jeff	20000.00	1
141	Drawings	drawings for wedding preparation	2020-08-14 12:33:23.278938	Jeff	2	Jeff	26000.00	1
147	USD Purchase	purchase of usd for int transactions and equipment purchase	2020-08-24 13:05:59.376647	Jeff	2	Jeff	70000.00	1
148	AC Repairs	ac repairs for the office	2020-08-26 19:06:15.25088	Idowu	2	Jeff	5000.00	1
149	salary payout	august salary payment for victoria	2020-08-27 12:02:35.916083	Jeff	2	Jeff	17000.00	2
150	Bonus Payout	Bonus payout for project participation and maptrackapp sales followup	2020-08-27 12:03:31.768208	Jeff	2	Jeff	50000.00	3
151	office utilities	office utilities purchase	2020-08-27 12:45:15.908255	Jeff	2	Jeff	8500.00	1
152	laptop charger	office laptop charger purchase	2020-08-28 16:26:28.712605	Jeff	2	Jeff	2500.00	1
153	car servicing	car service and repairs	2020-08-29 15:44:58.902199	Jeff	2	Jeff	12000.00	1
154	Cloud server payment	payment for cloud server for operations	2020-08-31 10:47:36.059917	Jeff	2	Jeff	13000.00	1
155	exp	office expenses	2020-08-31 10:50:04.387582	Jeff	2	Jeff	10000.00	1
156	internet subscription	office internet subscription renewal	2020-09-01 13:16:20.576687	Jeff	2	Jeff	16000.00	1
157	exp	for office expenses	2020-09-02 10:36:32.571964	Jeff	2	Jeff	10000.00	1
158	exp	expenses for fueling, sms purchase and utilities	2020-09-04 11:28:03.847957	Jeff	2	Jeff	12000.00	1
159	UI designs Fee	payment for UI designs for leape	2020-09-04 13:39:58.72343	Jeff	2	Jeff	50000.00	1
160	gen repair	office generator repairs	2020-09-09 13:45:38.510188	Jeff	2	Jeff	10000.00	1
161	drawings	drawings for wedding expenses	2020-09-09 14:30:52.582327	Jeff	2	Jeff	60000.00	1
162	shipment delivery	payment for sms server shipment delivery	2020-09-10 10:29:31.956839	Jeff	2	Jeff	6651.00	1
163	Car tire purchase	payment for car tire replacement 	2020-09-10 10:30:06.7523	Jeff	2	Jeff	10000.00	1
164	Drawings	made drawings for travel expense	2020-09-11 15:20:48.171969	Jeff	2	Jeff	20000.00	1
165	Drawings	for wedding expenditures	2020-09-14 20:07:12.234982	Jeff	2	Jeff	35000.00	1
166	exp	office expenses	2020-09-16 14:51:09.862734	Jeff	2	Jeff	10000.00	1
167	vat payout	vat for september	2020-09-18 11:56:46.936779	Jeff	2	Jeff	4950.00	5
168	exp	expenditure for operations	2020-09-18 12:02:23.409055	Jeff	2	Jeff	16400.00	1
169	tracker installation fee	tracker installation fee	2020-09-19 18:58:46.740114	Jeff	2	Jeff	3000.00	1
170	office exp	office exp	2020-09-19 18:59:10.400484	Jeff	2	Jeff	7000.00	1
171	exp	office exp	2020-09-24 12:06:11.431292	Jeff	2	Jeff	10000.00	1
172	car repairs	car repairs and fixings	2020-09-24 12:06:42.964394	Jeff	2	Jeff	10000.00	1
173	Domain rewawa;	Ecardex domain renewal	2020-09-25 11:38:17.181575	Jeff	2	Jeff	5070.00	1
174	Internet sub	Internet sub	2020-09-25 11:38:38.714165	Jeff	2	Jeff	12000.00	1
175	office expenses	office expenses	2020-09-28 18:43:03.742215	Jeff	2	Jeff	16200.00	1
176	Salary	Salary payment for Victoria Bolten	2020-09-28 18:43:32.773468	Jeff	2	Jeff	17000.00	1
177	Salary	Salary payment for sepember	2020-09-28 18:43:56.398831	Jeff	2	Jeff	50000.00	1
178	office exp	office expenditure	2020-10-01 09:38:59.04868	Jeff	2	Jeff	17000.00	1
179	laptop ba3	purchase of laptop ba3	2020-10-02 16:01:01.265667	Jeff	2	Jeff	10000.00	1
180	Drawing	made drawing for personal exp	2020-10-02 16:01:40.836593	Jeff	2	Jeff	53000.00	1
181	tracker installation fee	tracker installation fee plus transport	2020-10-03 10:48:29.377225	Jeff	2	Jeff	5000.00	1
182	exp	exp	2020-10-03 10:49:13.760438	Jeff	2	Jeff	5000.00	1
183	exp	expenditure for office activity	2020-10-04 10:46:09.496872	Jeff	2	Jeff	10000.00	1
184	drawing	made  a drawing for my wedding exp	2020-10-06 14:15:24.577765	Jeff	2	Jeff	30000.00	1
185	ADV Salary	salary advance payment	2020-10-06 14:15:55.939717	Jeff	2	Jeff	15000.00	1
186	drawings	drawing for wedding preparations	2020-10-08 19:50:41.441211	jeff	2	Jeff	140000.00	1
187	exp	expenses	2020-10-08 19:51:35.626545	Jeff	2	Jeff	10000.00	1
188	laptop battery	purchase for laptop ba3	2020-10-16 09:43:05.920635	Jeff	2	Jeff	10000.00	1
189	printer ink	printer ink replacement	2020-10-28 14:00:56.665534	jeff	2	jeff	9000.00	1
191	exp	office expenses	2020-10-28 14:14:52.744468	jeff	2	jeff	10000.00	1
190	drawing	drawing	2020-10-28 14:01:28.271687	jeff	2	Jeff	25000.00	1
192	october salary	for both victor and victoria	2020-10-28 14:15:43.088689	jeff	2	jeff	47000.00	1
193	exp	general exp	2020-10-31 12:47:35.613222	Jeff	2	Jeff	15000.00	1
194	vat remittance oct	october vat remittance	2020-11-03 09:54:40.218841	Jeff	2	Jeff	15937.50	5
195	Server payment	Production Server payments for October -- digital ocean	2020-11-03 10:50:01.21717	Jeff	2	Jeff	17550.00	1
196	exp	opex expenditure	2020-12-21 08:27:17.859308	jeffrey	2	Jeff	10000.00	1
197	Office relocation	Office relocation exp	2020-12-21 08:28:34.860327	Jeff	2	Jeff	15000.00	1
198	loan repayment	balance payment for a loan collected	2021-01-01 14:25:56.473621	Jeff	2	Jeff	50000.00	4
199	December salary	December salary balance payment	2021-01-01 14:26:40.85174	Victoria	2	Jeff	7000.00	2
200	exp	expenditures	2021-01-02 17:03:37.026471	Jeff	2	Jeff	10000.00	1
201	exp	exp for biz opperations	2021-01-06 08:03:52.203916	Jeff	2	Jeff	10000.00	1
641	opex	opex	2024-08-14 17:09:59.385931	Jeff	2	Jeff	12000.00	1
202	exp	expenditure for gen repairs and office utlities	2021-01-09 11:51:17.078275	Jeff	2	Jeff	15000.00	1
203	Exp	payment for job bonus  referral	2021-01-11 12:56:57.938513	Jeff	2	Jeff	150000.00	1
204	drawings	made drawings to fund bnc ventures	2021-01-11 12:57:39.643414	Jeff	2	Jeff	150000.00	1
207	exp	office exp and utilities 	2021-01-11 15:23:39.117984	Jeff	2	Jeff	10000.00	1
208	exp	kore wedding photos balance payment	2021-01-13 10:33:27.479076	jeff	2	Jeff	50000.00	4
209	exp	purchase equipment 	2021-01-13 10:53:16.191796	Jeff	2	Jeff	100000.00	1
210	exp	another expenditure for service delivery	2021-01-14 05:24:36.921546	Jeff	2	Jeff	25000.00	1
211	exp	part payment for office table making	2021-01-15 13:37:51.323672	Jeff	2	Jeff	12000.00	1
212	exp	work monitor 	2021-01-15 17:50:14.162258	Jeff	2	Jeff	16000.00	1
213	exp	for beverages purchase	2021-01-16 13:05:05.442986	Jeff	2	Jeff	4000.00	1
214	exp	operations expenditure	2021-01-17 14:46:31.948231	Jeff	2	Jeff	10000.00	1
215	exp	office opex and tracker installer fee	2021-01-19 11:05:46.117965	Jeff	2	Jeff	14000.00	1
216	opex	opex withdrawal	2021-01-20 11:42:45.298759	Jeff	2	Jeff	15000.00	1
217	opex	office expenditure 	2021-01-21 16:08:47.89042	Jeff	2	Jeff	30000.00	1
218	china shipment	shipment from china for goods 	2021-01-25 09:59:55.986318	Jeff	2	Jeff	119764.00	1
219	softloan	softloan to Jeff	2021-01-25 13:32:00.675526	Jeff	2	Jeff	50000.00	4
223	Bonus	Bonus for new tracker customers	2021-02-01 10:11:45.533401	Victoria Bolton	2	Jeff	16000.00	1
222	Tracker intallation 	One device tracker installation	2021-02-01 10:10:03.224396	Ogudu Tracker Installer	2	Jeff	3000.00	1
221	January Salary	Payment of january salary	2021-01-30 23:30:44.006741	Victoria Bolton	2	Jeff	17000.00	2
220	Tracker Installation Payment	payment for 5 tracker device installation	2021-01-30 21:10:01.4804	Ogudu	2	Jeff	15000.00	1
224	loan repayment	load repayment for tracker device purchase	2021-02-01 22:41:05.638773	Uzodinma Hezekiah	2	Jeff	50000.00	1
225	opex	opex withdrawal	2021-02-01 22:41:28.434292	Jeff	2	Jeff	10000.00	1
226	exp	car repairs	2021-02-05 10:30:54.057533	Jeff	2	Jeff	16000.00	1
227	internet device	internet device purchase for office operations	2021-02-08 09:53:20.981817	Jeff	2	Jeff	20000.00	1
228	opex	office opex	2021-02-08 09:57:07.247376	Jeff	2	Jeff	20000.00	1
229	phone repairs	phone screen repairs	2021-02-08 09:58:40.181833	Jeff	2	Jeff	10000.00	1
230	vat remitance	vat for January transactions 	2021-02-09 10:44:40.636614	Jeff	2	Jeff	19725.00	5
231	opex	opex	2021-02-12 09:12:56.091383	Jeff	2	Jeff	10000.00	1
232	opex	shipping clearance fee	2021-02-12 09:15:19.199843	NBC Cargo Logistics	2	Jeff	139956.00	1
233	opex	opex	2021-02-12 10:57:26.639682	Jeff	2	Jeff	10000.00	1
234	Internet sub	Opex internet sub for the office	2021-02-12 12:52:23.200504	Jeff	2	Jeff	19000.00	1
235	opex	opex	2021-02-14 17:47:48.122144	Jeff	2	Jeff	20000.00	1
236	Tracker installation	Tracker installation fee 	2021-02-15 18:17:23.056828	Ogudu	2	Jeff	5000.00	1
237	drawing	drawing for urgent expenses	2021-02-17 20:06:55.276024	Jeff	2	Jeff	50000.00	1
238	opex	opex 	2021-02-18 10:00:46.332665	Jeff	2	Jeff	10000.00	1
239	opex	purchese for propject development	2021-02-22 11:26:40.127461	Jeff	2	Jeff	15000.00	1
240	opex	purchase of raspberry toolkit	2021-02-22 11:28:49.486893	Jeff	2	Jeff	48000.00	1
241	opex	opex	2021-02-24 12:25:04.493867	jeff	2	Jeff	10000.00	1
242	cargo shipment clearing	cargo shipment clearing	2021-02-25 09:57:14.543346	NBC logistics	2	Jeff	49914.00	1
243	opex 	for fuel and exp	2021-03-01 15:11:01.222729	Jeff	2	Jeff	19500.00	1
244	Feb Salary	feb salary payment 	2021-03-01 15:11:31.288866	Victoria	2	Jeff	17000.00	2
245	Legal Document	Terms and condition documents and privacy policy for maptrackapp part payment	2021-03-01 15:13:05.662548	Bar Tosin	2	Jeff	20000.00	1
246	opex	purchase of beverages and others	2021-03-03 08:32:46.222373	Jeff	2	Jeff	12000.00	1
247	opex	digitalocean server payment	2021-03-03 10:16:41.968114	Jeff	2	Jeff	12586.95	1
248	opex	tracker installation fee	2021-03-05 16:38:19.45519	Ogudu	2	Jeff	9000.00	1
249	opex	opex 	2021-03-06 12:05:48.681344	Jeff	2	Jeff	15000.00	1
250	opex	opex	2021-03-07 12:22:53.914112	Jeff	2	Jeff	10000.00	1
251	installation fee	payment for tracker installation	2021-03-09 12:11:31.179854	ogudu	2	Jeff	4000.00	1
252	feb vat payout	vat for febuary transactions	2021-03-09 13:32:19.990811	jeff	2	Jeff	5325.00	5
253	opex	balance payment for office table making	2021-03-09 22:21:46.572691	Oladipupo Kazeem	2	Jeff	4000.00	1
254	fuel 	fuel purchase for operations	2021-03-11 20:07:58.503489	Jeff	2	Jeff	8500.00	1
255	Ecommerce Refund	Refund to customer on a transaction 	2021-03-11 20:12:03.552295	Oingtim gambo	2	Jeff	12000.00	1
256	opex	opex	2021-03-11 22:49:04.958406	Jeff	2	Jeff	10000.00	1
258	Internet subscription	office internet subscription	2021-03-12 11:17:50.761196	jeff	2	Jeff	18500.00	1
259	Generator repairs	Office generator repairs	2021-03-12 12:25:05.092497	Dauda	2	Jeff	5000.00	1
257	car repairs	car repairs for mobility	2021-03-12 11:17:19.102323	Jeff	2	Jeff	28000.00	1
260	opex	opex	2021-03-15 13:24:10.052252	Jeff	2	Jeff	12000.00	1
261	shippment fee	shippment fee for ecommerce	2021-03-16 08:27:45.730333	NBC 	2	Jeff	4880.00	1
262	drawings	for change of name processing with legal	2021-03-16 08:37:49.366855	jeff	2	Jeff	16000.00	1
263	shipment fee	shipment fee purchases from china	2021-03-17 13:59:02.492467	Go Express To Door Service	2	Jeff	4275.00	1
264	usd purchase 	usd purchase for ecommerce transasctions	2021-03-18 21:19:00.937757	jeff	2	Jeff	40000.00	1
265	Shipment	Shipment for eccormerce to abuja	2021-03-20 12:58:11.057962	AB logistics	2	Jeff	3000.00	1
266	Travel exp	exp for transportation and mobility	2021-03-28 10:12:57.313693	Jeff	2	Jeff	25000.00	1
267	Shipment	shipment fee payment for Raspevery pi and electrical equip	2021-03-28 10:15:01.306253	Mac-Kaf links	2	Jeff	20000.00	1
268	Fuel	office fuel consumption	2021-03-30 10:21:41.038202	Jeff	2	Jeff	8500.00	1
269	shippment	payment for shipment	2021-03-31 11:32:43.407841	NBC Skye Logistics	2	Jeff	39312.00	1
270	Salary	Salary and bonus  for Victoria	2021-03-31 11:33:30.152739	Victoria	2	Jeff	19500.00	2
271	reinbursement	reinbursement for office utility exp	2021-03-31 11:34:12.872871	Victoria	2	Jeff	1500.00	1
272	Traker installation	payment for tracker installation	2021-04-02 18:04:43.982814	Ogudu	2	Jeff	14000.00	1
273	server payment	payment for march usage	2021-04-03 14:24:44.398372	Jeff	2	Jeff	13831.95	1
274	March Vat 	march vat remittance	2021-04-08 11:15:28.37756	Firs	2	Jeff	5512.00	5
275	Airtime and sim purchase	airitme and sim purchase for the tracker	2021-04-08 11:15:59.117191	Jeff	2	Jeff	6000.00	1
277	Opex	opex for exp	2021-04-08 14:29:29.511404	Jeff	2	Jeff	10000.00	1
276	shipment	nbc shipment payment from china	2021-04-08 14:29:04.93096	NBC Skye Logistics	2	Jeff	30240.00	1
278	Tracker device installation	tracker device installation	2021-04-09 13:18:49.571712	Ogdudu	2	Jeff	4000.00	1
279	opex	opex	2021-04-12 19:42:03.669983	Jeff	2	Jeff	10000.00	1
280	Opex	opex exp	2021-04-17 11:42:09.272782	Jeff	2	Jeff	10000.00	1
281	Fuel purchase	fuel for operations	2021-04-17 11:42:47.081614	Jeff	2	Jeff	10000.00	1
282	opex	opex	2021-04-18 14:36:10.522063	Jeff	2	Jeff	10000.00	1
283	office equipment purchase	purchase of inverter batteries and inverter machine equipment	2021-04-18 19:27:51.0376	Jeff	2	Jeff	125000.00	1
284	electricity wiring	payment for electrical wiring	2021-04-21 08:23:54.702049	Biola	2	Jeff	3000.00	1
285	office equipment	purchase of electrical fan	2021-04-21 08:24:39.616523	Jeff	2	Jeff	23000.00	1
286	opex	opex 	2021-04-21 14:18:21.489041	Jeff	2	Jeff	10000.00	1
287	opex	opex 	2021-04-23 13:46:50.320768	Jeff	2	Jeff	10000.00	1
288	repairs	car repair and gen repairs	2021-04-26 15:26:04.107066	Jeff	2	Jeff	16950.00	1
289	Tracker Installation	fixing and repairs of the tracker devices	2021-04-26 15:26:44.137499	Jeff	2	Jeff	3000.00	1
290	opex	opex 	2021-04-27 18:58:46.113655	Jeff	2	Jeff	10000.00	1
291	Salary Payment	payment for april salary	2021-04-27 18:59:14.090352	Jeff	2	Jeff	20000.00	1
292	nbc shipment	payment for shipment form china	2021-04-27 20:17:33.0836	NBC Sky logistics	2	Jeff	1830.00	1
293	domain name purchase	purchase of domain name Mesagine.com	2021-04-27 20:18:08.045952	Jeff	2	Jeff	4000.00	1
294	office internet	modem for universal sim and ink refill plus keyboard	2021-04-28 11:37:58.326532	Jeff	2	Jeff	21500.00	1
296	opex	opex for business activity	2021-04-30 17:01:24.95771	Jeff	2	Jeff	10000.00	1
297	opex	opex	2021-05-05 10:54:40.552164	Jeff	2	Jeff	10000.00	1
298	internet sub	internet sub for vdt	2021-05-05 10:55:06.211831	Jeff	2	Jeff	10500.00	1
299	opex	opex	2021-05-06 16:36:44.049535	Jeff	2	Jeff	10000.00	1
300	cloud server	cloud server payment for may	2021-05-07 14:01:59.901888	Jeff	2	Jeff	12000.00	1
301	opex	opex	2021-05-10 19:36:43.115943	Jeff	2	Jeff	10000.00	1
302	iot camera	equipment for product dev	2021-05-12 08:09:45.410444	Jeff	2	Jeff	13000.00	1
303	opex	opex	2021-05-15 09:34:16.561751	Jeff	2	Jeff	15000.00	1
304	opex	opex	2021-05-15 09:43:08.454674	Jeff	2	Jeff	15000.00	1
305	usd purchase	usd for cloud server	2021-05-17 09:43:22.616223	Jeff	2	Jeff	74600.00	1
306	Vat for april	vat remmitance for the month of april	2021-05-17 09:43:50.016162	Jeff	2	Jeff	6500.00	1
307	office expenses	purchase of window blinds -- part payment\r\n.	2021-05-18 12:12:03.542346	Jeff	2		10000.00	1
308	office exp	exp for utilities	2021-05-23 12:01:10.5355	Jeff	2	Jeff	20000.00	1
309	opex	opex	2021-05-27 11:35:55.389476	Jeff	2	Jeff	10000.00	1
310	internet sub	internet subscription for june	2021-05-31 12:26:22.991203	Jeff	2	Jeff	10500.00	1
311	may salary	salary payment for victoria	2021-06-03 10:14:52.523667	Jeff	2	jeff	20000.00	1
312	opex	opex 	2021-06-07 16:09:16.709758	Jeff	2	Jeff	20000.00	1
313	tracker installation	payment for tracker installation	2021-06-13 17:31:43.737534	ogudu	2	Jeff	6000.00	1
314	opex	opex	2021-06-14 09:28:06.057044	Jeff	2	Jeff	20000.00	1
315	vat remmitance May	vat remttance for may	2021-06-15 09:13:13.24847	Jeff	2	Jeff	5000.00	1
316	Delivery and clearing fee	Delivery and clearing fee	2021-06-16 14:51:50.553109	Nbc Skye	2	Jeff	111334.00	1
295	purchase of bags	product purchase from china (bag)	2021-04-28 11:41:56.391519	Jeff	2	Jeff	103700.00	1
317	opex	opex	2021-06-24 10:22:10.18935	Jeff	2	Jeff	10000.00	1
318	opex	opex	2021-06-25 17:50:31.367895	Jeff	2	Jeff	8000.00	1
320	Opex	opex	2021-07-04 20:23:16.997184	Jeff	2	Jeff	12000.00	1
321	delivery fee	delivery fee for ecommerce	2021-07-04 20:23:47.466795	Jeff	2	Jeff	2500.00	1
319	Opex	airtime for the tracker sims	2021-07-01 15:30:49.934239	Jeff	2	Jeff	4000.00	1
322	car repairs	car repairs	2021-07-05 19:57:06.562678	Jeff	2	Jeff	15000.00	1
323	Car repairs	car alignment and wheel balancing	2021-07-06 18:54:12.781348	Jeff	2	Jeff	4000.00	1
324	electric recharges	electric recharges	2021-07-14 19:29:49.402635	Jeff	2	Jeff	12000.00	1
325	opex	withdrawal for opex	2021-07-17 09:42:14.15649	Jeff	2	Jeff	10000.00	1
326	contibutions	weekly contibutions	2021-07-17 09:42:45.955291	Jeff	2	Jeff	5000.00	1
327	car repairs	car repairs balance	2021-07-17 12:29:36.828874	Ayoola	2	Jeff	6000.00	1
328	loan for rent	loan for rent payment	2021-07-21 20:56:29.522133	Jeff	2	Jeff	400000.00	1
329	shipment of device	shipment of device from china	2021-07-22 10:39:22.092427	NBC SKYE logistics	2	Jeff	1253.00	1
330	opex	withdrawals for opex	2021-07-28 15:15:35.921842	Jeff	2	Jeff	10000.00	1
331	purchse of bank seal	purchase of bank seal	2021-08-03 10:22:24.179914	Jeff	2	Jeff	6000.00	1
332	opex	opex 	2021-08-05 16:55:34.246399	Jeff	2	Jeff	10000.00	1
333	opex	purchase of samples 	2021-08-10 11:07:09.420729	jeff	2	Jeff	48000.00	1
334	opex	ads payment	2021-08-11 10:24:55.236883	fb ads	2	Jeff	31000.00	1
335	september expenditure	expenditures made in september	2021-09-30 09:09:52.082616	Jeff	2	Jeff	490849.59	1
336	aug exp	aug exp registration	2021-08-31 09:19:06.402896	Jeff	2	Jeff	43653.08	1
337	fb ads payment	payment for ads on facebok	2021-10-01 09:25:12.28311	Jeff	2	Jeff	20000.00	1
338	exp	opex expenses	2021-10-01 09:30:14.806609	Jeff	2	Jeff	10000.00	1
339	Clearance payment	shipment clearance payment for trackers and laptop bags	2021-10-01 09:39:18.106349	NBC SKE	1	Jeff	173160.00	1
340	electricity bill	electricity bill	2021-10-01 17:24:36.59982	Jeff	2	Jeff	5000.00	1
341	medical bills	medical bills	2021-10-02 08:54:41.979867	Jeff	2	Jeff	30000.00	1
342	gen repair	generator repair	2021-10-05 13:06:25.152529	jeff	2	Jeff	5000.00	1
343	opex 	opex	2021-10-07 09:43:35.67327	jeff	2	Jeff	10000.00	1
344	Opex	payment for operations exp	2021-10-12 09:32:23.119254	Jeff	2	Jeff	10000.00	1
345	2020 book filings	payment for book filings	2021-10-12 09:34:25.198946	Damilola 	2	Jeff	30000.00	1
346	token purchase	opex	2021-10-15 12:34:54.771625	Jeff	2	Jeff	3000.00	1
347	medical bills	medical bills	2021-10-17 12:52:40.723309	Jeff	2	Jeff	20000.00	1
348	fb ads	payment for fb ads	2021-10-19 08:16:12.497758	Jeff	2	Jeff	27000.00	1
349	maptrackapp tc p2	balance payment for maptrackapp terms and conditions	2021-10-20 08:42:04.54821	Tosin	2	Jeff	10000.00	1
350	laptop bag restock	laptop bag restock	2021-10-21 14:31:54.832636	Jeff	2	Jeff	98000.00	1
351	opex	opex exp	2021-10-21 18:27:49.056789	jeff	2	Jeff	10000.00	1
352	opx	opex	2021-10-22 19:10:01.791185	Jeff	2	Jeff	10000.00	1
353	playstore account	google playstore account	2021-10-23 09:51:01.416502	Jeff	2	Jeff	12000.00	1
354	zenith bank chrges	zenith bank corporate account opening charges	2021-10-25 15:17:40.577354	Jeff	2	Jeff	9000.00	1
355	opex	opex	2021-10-25 19:10:54.967491	Jeff	2	Jeff	6000.00	1
356	miscellious	payment for bcert	2021-10-27 08:51:41.179993	Jeff	2	Jeff	10000.00	4
357	opex	opex	2021-10-27 08:51:54.439997	Jeff	2	Jeff	12000.00	1
358	car repairs	car repairs and servicing	2021-10-28 09:29:07.141956	Jeff	2	Jeff	20000.00	1
359	opex	internet and fb ads	2021-10-31 13:22:10.426422	Jeff	2	Jeff	30000.00	1
360	Opex	Opex	2021-10-31 13:22:30.425931	Jeff	2	Jeff	10000.00	1
361	cloud server	payment for cloud server sub	2021-11-04 09:11:47.325534	Jeff	2	Jeff	7500.00	1
362	opex	opex 	2021-11-04 17:00:55.036693	jeff	2	Jeff	5000.00	1
363	exp	opex exp	2021-11-06 09:48:34.021735	Jeff	2	Jeff	6000.00	1
364	opex	exectcity and  opex	2021-11-09 10:20:53.290137	Jeff	2	Jeff	16000.00	1
365	opex	opex	2021-11-14 12:36:16.570393	Jeff	2	Jeff	20000.00	1
366	drawing	made drawing	2021-11-16 12:23:53.951401	Jeff	2	Jeff	95000.00	4
367	fuel	purchase of fuel	2021-11-17 07:51:39.576847	Jeff	2	Jeff	15000.00	1
368	video ad	payment for video ads - part payment	2021-11-22 10:48:10.714383	Ikenna Ukonu Egbe	2	Jeff	5000.00	1
369	gen repairs	generator repair	2021-11-24 11:35:50.706288	Jeff	2	Jeff	10000.00	1
370	cloud server	cloud server advance payment	2021-11-25 08:59:50.527353	Jeff	2	jeff	50000.00	1
371	drawings	made drawings for trip to abuja	2021-11-26 09:31:32.392443	Jeff	2	Jeff	50000.00	1
372	exp	paid for a purchase	2021-12-04 11:19:57.137043	Jeff	2	Jeff	13000.00	1
373	drawings	made drawings	2021-12-08 08:27:36.530239	Jeff	2	Jeff	45000.00	1
374	tracker servicing	tracker servicing	2021-12-10 14:15:31.799169	Jeff	2	Jeff	2000.00	1
375	internet sub	internet sub	2021-12-10 14:15:53.619781	Jeff	2	Jeff	12000.00	1
376	thermal printer purchase	purchase of thermal printer for pos project	2021-12-13 13:13:02.031348	Jeff	2	Jeff	18000.00	1
377	exp	opex	2021-12-16 05:35:22.745838	Jeff	2	Jeff	20000.00	1
378	opex	opex	2021-12-18 19:24:55.60137	Jeff	2	Jeff	20000.00	1
379	tracker servicing	tracker servicing	2021-12-22 14:32:57.752589	Ogudu	2	Jeff	5500.00	1
380	exp	exp	2021-12-22 14:33:16.352374	Jeff	2	Jeff	20000.00	1
381	drawings	made drawings for exp	2021-12-23 10:20:19.199324	Jeff	2	Jeff	90000.00	1
382	opex	opex since jan	2022-01-05 15:41:37.796822	jeff	2	Jeff	40000.00	1
383	maptrackapp domain renewal	payment for maptrackapp domain renewal	2022-01-06 12:04:24.932203	Jeff	2	Jeff	8505.00	1
384	opex jana8th	opex withdrawal	2022-01-08 15:08:24.437006	Jeff	2	jeff	10000.00	1
385	Opex Jan14th	Opex withdrawal on jan14th	2022-01-14 17:42:26.523004	Jeff	2	Jeff	10000.00	1
386	opex jan 3rdweek	opex withdrawal 3rd week	2022-01-17 11:01:52.20083	Jeff	2	Jeff	15000.00	1
387	mpos device	mpos device for sales pnt product development	2022-01-19 09:06:03.412641	Jeff	2	Jeff	23000.00	1
388	opex	for gen repairs	2022-01-19 13:07:03.272881	Jeff	2	Jeff	10000.00	1
389	opex	opex for jan 3rd week	2022-01-23 19:22:50.631802	Jeff	2	Jeff	15000.00	1
390	tracker sim purchase	purchase of tracker sim	2022-01-26 18:19:08.787021	Jeff	2	Jeff	20000.00	1
391	repairs and internet	repairs and internet	2022-01-28 11:38:13.472358	Jeff	2	Jeff	35000.00	1
392	opex exp	opex expenditures	2022-01-31 14:02:14.685197	Jeff	2	Jeff	15000.00	1
393	feb fuel	fuel purchase for febuary	2022-02-04 11:26:47.867536	jeff	2	Jeff	20000.00	1
394	tracker installation	payment for tracker installation fee	2022-02-06 09:39:54.17178	Ogudu Friday	2	Jeff	8000.00	1
395	drawing	made a drawings	2022-02-11 10:17:35.204102	Jeff	2	Jeff	30000.00	1
396	opex	opex	2022-02-12 10:33:51.710183	Jeff	2	Jeff	20000.00	1
397	opex	opex	2022-02-18 18:33:35.142606	Jeff	2	Jeff	10000.00	1
398	opex	opex	2022-02-25 12:48:33.912478	jeff	2	Jeff	25000.00	1
399	AT89C2051 Programmer	purchase of microcontrollers	2022-02-25 12:52:56.286343	Jeff	2	Jeff	8000.00	1
400	opex 25thfeb	opex	2022-02-25 19:18:21.022088	Jeff	2	Jeff	10000.00	1
401	internet sub	internet sub	2022-03-02 10:21:11.779657	Jeff	2	Jeff	10000.00	1
402	shipment payment	shipment payment for laptop shipment from america	2022-03-05 08:44:47.770014	Jeff	2	Jeff	47000.00	1
403	emembeded components	purchase of components	2022-03-27 10:45:40.13787	Jeff	2	Jeff	45000.00	1
404	miscellenous	miscellenous	2022-03-27 10:46:14.038917	Jeff	2	Jeff	25000.00	1
405	opex	opex	2022-03-27 10:47:19.144502	Jeff	2	Jeff	10000.00	1
406	soft loan	soft loan	2022-03-27 10:48:23.308182	Jeff	2	Jeff	35000.00	1
407	digital ocean	payment for server	2022-03-31 10:00:48.241364	Jeff	2	Jeff	15000.00	1
408	exp	refund back soft loan	2022-04-14 08:40:21.551574	Jeff	2	Jeff	20000.00	1
409	exp	short loan refund	2022-04-23 10:07:09.377375	Victor	2	Jeff	15000.00	1
410	exp	expenditures for necessities	2022-04-23 10:09:40.707458	Jeff	2	Jeff	7000.00	1
411	exp	payment for ba3 repairs	2022-04-27 09:42:10.312438	Jeff	2	Jeff	3000.00	1
412	exp	expenditure for opex	2022-04-29 14:25:54.042255	Jeff	2	JEff	8500.00	1
413	backend dev	first payment of backend development	2022-07-07 17:54:24.817198	Kelvin Egoba	2	Jeff	100000.00	1
414	debt repayment	debt repayment to mr Ayodeji uzodinma	2022-08-05 10:43:27.38381	mrs Ayodeji	2	Jeff	100000.00	1
415	laptop repairs	laptop repairs	2022-08-05 10:43:48.716748	Jeff	2	Jeff	20000.00	1
416	inverter purchase	inverter purchase 	2022-08-05 10:44:17.099793	Jeff	2	Jeff	115000.00	1
417	inverter installation	inverter installation	2022-08-05 11:16:23.919771	Solomon	2	Jeff	6500.00	1
418	laptop battery	laptop battert purchase	2022-08-06 09:17:53.36455	Jeff	2	Jeff	20000.00	1
419	internet	internet sub	2023-01-19 17:05:05.280162	Jeff	2	Jeff	15000.00	1
420	accounting fee	fee for book filing and end of year books preparation	2023-01-23 11:12:33.780517	Akinbowale Taiwo	2	Jeff	70000.00	1
421	internet	internet sub	2023-01-30 20:17:40.577254	Jeff	2	Jeff	16500.00	1
422	shipment fee	shipment fee for laptop bags	2023-02-01 16:45:34.644933	E & C De yahannce united express	2	Jeff	77950.00	1
423	auditor fee	first deposit for annual audit and filing	2023-02-03 15:18:01.292065	socium cloud accounting	2	Jeff	100000.00	1
424	opex	payment for dispatch delivery	2023-02-03 20:29:14.181455	Banks Logistics	2	Jeff	4500.00	1
425	Ikedc feb	Ikeja electric bill	2023-02-13 06:17:36.232872	Jeff	2	Jeff	12000.00	1
426	drawing	made a drawing	2023-02-18 21:10:22.900262	Jeff	2	Jeff	40000.00	1
427	internet sub	purchase for internet sub	2023-02-18 21:10:59.51781	Jeff	2	Jef	15000.00	1
428	audit second payment	second installment payment for anual audit	2023-02-23 11:17:10.841269	Sociumumb	2	Jeff	100000.00	1
429	tax remittance	tax remittance and penalty charges	2023-02-23 11:17:53.171103	Socium cloud accounting	2	Jeff	60300.00	1
430	fuel purchase	fuel for office operations	2023-04-05 12:23:25.901113	Jeff	2	Jeff	10000.00	1
431	cash exchange	cash exchange	2023-04-05 12:24:04.470779	Jeff	2	Jeff	10000.00	1
432	personal tax filing fee	payment for personal tax filing fee	2023-04-07 11:03:18.967287	Socium cloud accounting	2	Jeff	40000.00	1
433	restock	laptop bag restock	2023-04-07 16:41:37.788953	Jeff	2	Jeff	105000.00	1
434	spectranet device 	isp spectranet device purchase	2023-04-10 19:07:06.370618	Jeff	2	Jeff	26000.00	1
435	fuel purchase	fuel and fiel gallon purchase	2023-04-21 16:15:21.125944	Jeff	2	Jeff	18000.00	1
436	exp	expenditure for miscellenous and gen repairs	2023-04-24 13:41:08.760086	Jeff	2	Jeff	12000.00	1
437	Loan	loan for product acquisition 	2023-04-27 09:01:51.326757	Jeff	2	Jeff	790000.00	1
438	Payee	lirs payee from 2020 to 2022	2023-04-27 13:45:21.967398	Jeff	2	Jeff	45000.00	1
439	ikeja electric	ikeja electric bill 	2023-05-01 08:33:37.944827	Jeff	2	Jeff	10000.00	1
440	utility bills	utility bills	2023-05-01 08:46:05.14127	Jeff	2	Jeff	17300.00	1
441	cloud server	digital ocean cloud sever	2023-05-01 09:21:15.181697	Jeff	2	Jeff	30000.00	1
442	24L laptop Bag	24L purchase of laptop bag	2023-05-04 13:41:03.076132	Jeff	2	Jeff	442800.00	1
443	shipment payment	payment for shipments from china	2023-05-06 12:56:06.486528	DE - YOHANNCE UNITED EXPRESS	2	Jeff	5180.00	1
444	internet sub	spectranet internet data sub	2023-05-10 12:28:52.75185	Jeff	2	jeff	20000.00	1
445	medical bills	medical bills	2023-05-12 08:40:42.68227	Jeff	2	Jeff	64550.00	1
446	reliance hmo	health insurance subscription	2023-05-15 08:40:07.789173	Jeff	2	Jeff	7000.00	1
447	payee penalty	payee penalty lirs charges	2023-05-15 17:15:28.448319	jeff	2	jeff	150000.00	1
448	office supplies	office supplies	2023-05-17 12:39:26.358163	Jeff	2	Jeff	14000.00	1
449	sihpment fee	shipment fee	2023-05-18 14:25:17.738337	Nbc skye logistics	2	jeff	4988.00	1
450	electrical fittings	electrical fittings	2023-05-21 10:55:24.896397	Abas Electrician	2	Jeff	7000.00	1
451	legal fees	legal fees for contract documentation	2023-05-22 08:42:31.881169	Tosin	2	Jeff	50000.00	1
452	design UI fees	design UI fees	2023-05-22 08:42:56.65593	Samson Illori	2	Jeff	50000.00	1
453	office equipment purchase	office equipment purchase	2023-05-22 11:13:42.53094	Jeff	2	Jeff	150000.00	1
454	tracker installation	tracker installation	2023-05-25 20:41:24.024755	Ogudu	2	Jeff	8000.00	1
455	utility payments	utility payments	2023-05-30 23:03:21.641494	Jeff	2	Jeff	20000.00	1
456	cloud server renewal	cloud sever renewals	2023-05-31 23:34:30.191849	Jeff	2	Jeff	37000.00	1
457	POS cash withdrawal	Pos cash withdrawal	2023-06-04 09:18:32.664496	Jeff	2	Jeff	10200.00	1
458	opex	opex	2023-06-04 09:18:51.571862	Jeff	2	Jeff	20000.00	1
459	car insurance payment	quarterly insurance payment	2023-06-05 11:22:37.928976	Axamansard insurance	2	Jeff	46000.00	1
460	usd purchase	usd purchase	2023-06-07 13:21:20.546837	Abubakar	2	Jeff	76100.00	1
461	pos trnsaction	pos transaction for  plumbing work payment	2023-06-07 15:13:48.339672	Jeff	2	Jeff	11300.00	1
462	opex	opex withdraws	2023-06-08 19:24:23.646779	Jeff	2	Jeff	20000.00	1
463	internet sub	spectranet internet subscription	2023-06-10 09:37:27.336324	Jeff	2	Jeff	20000.00	1
464	clearance fee	clearance fee from DE - YOHANNCE UNITED EXPRESS	2023-06-10 12:51:41.272504	DE - YOHANNCE UNITED EXPRESS	2	Jeff	10925.00	1
465	purchase of laptop bag	purchase of laptop bag	2023-06-11 08:52:49.72082	Jeff	2	Jeff	63000.00	1
466	opex	opex	2023-06-13 15:09:57.8116	Jeff	2	Jeff	15000.00	1
467	OPex	opex	2023-06-15 09:26:20.522158	Jeff	2	Jeff	15000.00	1
468	opex	opex	2023-06-25 09:01:20.631588	Jeff	2	Jeff	10000.00	1
469	shipment fee	shipment fee	2023-06-25 09:03:39.57681	NBC Skye	2	Jeff	13947.00	1
470	gig logistics setup	gig logistics account setup	2023-06-26 10:37:53.826221	GIGLogisics	2	Jeff	6000.00	1
471	opex	opex	2023-06-27 12:36:14.437571	Jeff	2	Jeff	20000.00	1
472	car repair parts	car repair part purchase	2023-06-29 14:08:42.489185	Mechanic	2	Jeff	10500.00	1
473	opex	opex	2023-06-29 14:08:56.951427	Jeff	2	Jeff	15000.00	1
474	opex	opex	2023-07-01 12:50:46.916489	Jeff	2	jeff	10000.00	1
475	usd purchase	usd purchase	2023-07-01 12:54:54.577175	Jeff	2	Jeff	80000.00	1
476	opex	opex	2023-07-04 09:33:22.297156	Jeff	2	Jeff	20000.00	1
477	rent	rent payment	2023-07-04 09:33:46.335758	Jeff	2	Jeff	550000.00	1
478	payment for fb ads	payment for fb ads for june	2023-07-07 09:52:53.197921	jeff	2	jeff	34176.00	1
479	opex	opex	2023-07-07 14:16:30.412347	Jeff	2	Jeff	25000.00	1
480	internet sub renewal	intenret sub renewal	2023-07-10 09:17:02.437731	Jeff	2	Jeff	20000.00	1
481	installation charges	tracker installation charges 	2023-07-11 12:30:34.241563	Ogudu	2	Jeff	11500.00	1
482	opex	opex 	2023-07-13 09:12:35.164163	Jeff	2	Jeff	10000.00	1
483	installation charges 	installation charges	2023-07-19 08:28:43.35677	Ogudu	2	Jeff	4000.00	1
484	opex	opex	2023-07-19 08:29:32.021982	Jeff	2	Jeff	15000.00	1
485	opex	opex	2023-07-29 11:15:13.85356	Jeff	2	Jeff	15000.00	1
486	shipment payment	shipment payment	2023-08-01 12:36:30.728056	Yohannce united express	2	Jeff	78600.00	1
487	shipment payment 	shipment payment 	2023-07-25 13:03:26.615818	DeYohannce united express	2	Jeff	300700.00	1
488	opex	opex	2023-08-02 10:40:29.428695	Jeff	2	Jeff	10000.00	1
489	opex	opex	2023-08-03 16:44:37.787051	jeff	2	Jeff	20000.00	1
490	opex	opex	2023-08-08 17:47:58.691204	Jeff	2	Jeff	20000.00	1
491	internet sub	internet sub	2023-08-09 09:10:19.573277	Jeff	2	Jeff	20000.00	1
492	laptop repair	laptop repair	2023-08-11 11:15:27.333635	Jeff	2	Jeff	20000.00	1
493	opex	opex	2023-08-11 13:42:13.674822	Jeff	2	Jeff	20000.00	1
494	shipment clearance	shipment clearance	2023-08-12 19:48:36.713382	Nbc skye logistics	2	Jeff	7000.00	1
495	fb ads	fb ads payment	2023-08-22 09:26:55.928413	Jeff	2	Jeff	29500.00	1
496	opex	opex	2023-08-24 08:21:44.328045	Jeff	2	Jeff	26000.00	1
497	opex	opex for utility and internet	2023-09-09 14:40:05.398905	Jeff	2	Jeff	45000.00	1
498	laptop battery	laptop battery purchase	2023-09-09 14:40:31.471958	Jeff	2	Jeff	17500.00	1
499	opex exp	opex exp	2023-09-15 09:04:17.171814	Jeff	2	Jeff	20000.00	1
500	opex	opex	2023-09-19 09:36:10.715609	Jeff	2	Jeff	15000.00	1
501	opex	opex	2023-09-28 12:52:18.470723	Jeff	2	Jeff	15000.00	1
502	opex	opex	2023-09-30 08:49:21.748395	Jeff	2	Jeff	30000.00	1
503	opex	opex	2023-10-01 07:37:16.753103	Jeff	2	Jeff	20000.00	1
504	opex	opex oct 2nd	2023-10-02 18:20:03.128276	Jeff	2	Jeff	25000.00	1
505	opex	opex	2023-10-06 09:29:10.395182	Jeff	2	Jeff	20000.00	1
506	opex	opex	2023-10-06 22:05:31.457627	Jeff	2	Jeff	30000.00	1
507	power and internet utility bill	power and internet utilities 	2023-10-08 10:32:47.80664	Jeff	2	Jeff	30000.00	1
508	opex	opex	2023-10-10 08:41:42.895544	Jeff	2	jeff	15000.00	1
509	opex	opex oct 11th 23	2023-10-11 09:48:54.790371	Jeff	2	Jeff	20000.00	1
510	opex	opex on oct 13th	2023-10-13 06:14:41.011146	Jeff	2	Jeff	45000.00	1
511	internet purchase	internet purchase. the previous purchase was not working	2023-10-18 08:57:54.083141	Jeff	2	Jeff	20000.00	1
512	opex	opex	2023-10-26 16:56:20.883848	Jeff	2	Jeff	20000.00	1
513	opex	opex oct 29th	2023-10-29 09:39:43.681364	Jeff	2	Jeff	30000.00	1
514	opex	opex	2023-11-02 13:34:34.108301	Jeff	2	jeff	40000.00	1
515	fb ads	fb ads	2023-11-04 21:38:48.727677	Jeff	2	Jef	30000.00	1
516	opex	opex 	2023-11-14 11:23:08.432125	biddybamaz logistics 	2	Jeff	13000.00	1
517	opex	opex	2023-11-16 10:44:45.676768	Jeff	2	Jeff	47000.00	1
518	opex	opex	2023-11-21 16:00:37.581514	Jeff	2	Jeff	20000.00	1
519	insurance renewal	one year insurance renewal	2023-11-21 21:59:27.345968	Jeff	2		15000.00	1
520	car vehicle licence renewal	annual vehicle license renewal	2023-11-25 07:14:28.996417	Jeff	2	Jeff	9000.00	1
521	baging and nylons	baggin and nylons	2023-11-25 07:15:02.34731	Jeff	2	Jeff	7500.00	1
522	cloud server renewal	cloud server renewal for mobifin	2023-11-26 11:02:20.312135	mobifin	2	jeff	125000.00	1
523	bed	semi orthopedic bed	2023-11-29 11:21:15.991832	Jeff	2	Jeff	119500.00	1
524	opex	opex	2023-11-29 11:47:10.13624	Jeff	2	Jeff	25000.00	1
525	cash refund for opex	cash rfund for opex	2023-12-01 12:08:28.501182	Jeff	2	Jeff	50000.00	1
526	uitility bills	utility bills	2023-12-01 12:10:13.781819	Jeff	2	Jeff	10000.00	1
527	refund invoice	invoice refund 	2023-12-01 18:13:31.441532	Uhegbu Emeka	2	Jeff	20000.00	1
528	paid engr	paid engr for installation work	2023-12-01 18:14:51.821223	Engr Karim Yakubu	2	Jeff	5000.00	1
529	opex 	opex 	2023-12-05 19:25:42.661425	Jeff	2	Jeff	20000.00	1
530	opex	payment of 45 usd for ads cost	2023-12-06 12:16:12.290755	Jeff	2	Jeff	62000.00	1
531	machinery equipment	car gear purchase	2023-12-08 20:47:20.907711	Jeff	2	Jeff	250000.00	1
532	fb ads payment	fb ads payment	2023-12-13 07:45:50.456939	Jeff	2	Jeff	56000.00	1
533	hmo renewal	hmo renewal	2023-12-13 09:17:56.647463	Jeff	2	Jeff	14000.00	1
534	delivery charges	delivery charges	2023-12-16 06:26:48.072383	Jeff	2	Jeff	24000.00	1
535	Socium audit balance payment	Socium audit balance payment	2023-12-19 10:27:34.696553	Socium cloud account	2	Jeff	40000.00	1
536	gen repairs	generator repairs	2023-12-19 14:19:05.686274	Jeff	2	Jeff	25000.00	1
537	fb ads	fb ads payment	2023-12-22 06:58:46.21798	Jeff	2	Jeff	82000.00	1
538	xmas bonus	xmas bonus	2023-12-23 10:16:15.1524	Jeff	2	Jeff	50000.00	1
539	opex	Opex dec 26th	2023-12-26 10:34:28.094004	Jeff	2	Jeff	25000.00	1
540	nepa uuid device	nepa uuid device purchase	2023-12-27 09:15:14.660996	Jeff	2	Jeff	25000.00	1
541	opex	opex	2023-12-28 14:50:07.269206	Jeff	2	Jeff	10000.00	1
542	miscellenous	miscellenous 	2023-12-29 08:48:05.547276	Jeff	2	Jeff	35000.00	1
543	opex	opex	2023-12-30 11:43:15.60246	Jeff	2	Jeff	10000.00	1
544	Opex	part opayment for room doors	2023-12-31 07:42:13.697587	Jeff	2	Jeff	30000.00	1
545	opex	opex	2024-01-01 11:17:37.511289	Jeff	2	Jeff	20000.00	1
546	exp	miscellenous exp	2024-01-05 11:09:04.953099	Jeff	2	Jeff	32900.00	1
547	exp	electricity recharge	2024-01-08 20:54:26.503284	Jeff	2	Jeff	10000.00	1
548	usd purchase	usd purchase	2024-01-10 13:07:12.292124	Jeff	2	Jeff	125000.00	1
549	electrical installation 	electrical installation charges	2024-01-11 19:38:30.883067	Abas Electrician	2	Jeff	50000.00	1
550	second term school fees	second term school fees	2024-01-15 08:32:13.402678	Ayodeji	2	Jeff	15000.00	1
551	opex	purchase of charge controller 	2024-01-15 12:28:18.356937	Jeff	2	Jeff	64000.00	1
552	packaging purchase	packaging purchase	2024-01-17 08:58:12.966862	Jeff	2	Jeff	17000.00	1
553	internet sub	internet sub	2024-01-17 09:20:44.431399	Jeff	2	Jeff	25000.00	1
554	opex	opex	2024-01-17 10:09:27.061385	Jeff	2	Jeff	20000.00	1
555	opex	opex	2024-01-18 14:26:14.007896	Jeff	2	JEff	20000.00	1
556	opex	payment for shipment	2024-01-18 14:27:36.596733	DE - YOHANNCE UNITED EXPRESS	2	Jeff	27905.00	1
557	opex	payment for shipment	2024-01-22 13:29:49.353142	NBC Skye	2	Jeff	6397.00	1
558	opex	opex	2024-01-23 08:11:03.591917	Jeff	2	Jeff	30000.00	1
559	opex	opex 	2024-01-24 00:37:44.11209	Jeff	2	Jeff	10000.00	1
560	opex	electricity bill	2024-01-26 22:39:53.636829	Jeff	2	Jeff	10000.00	1
561	opex	shipment and clerance charges	2024-01-28 20:31:36.60375	NBC Skye Logistics	2	Jeff	8776.00	1
562	opex	opex	2024-01-30 16:20:54.09276	Jeff	2	Jeff	40000.00	1
563	utility and repairs	utility and repairs	2024-02-01 08:08:48.351422	Jeff	2	Jeff	18000.00	1
564	opex	opex	2024-02-02 10:10:01.252193	Jeff	2	Jeff	20000.00	1
565	opex	opex	2024-02-05 09:15:16.097394	jeff	2	Jeff	75000.00	1
566	opex 	opex and baby food	2024-02-09 09:08:17.548278	Jeff	2	Jeff	56000.00	1
567	opex	opex	2024-02-10 11:25:50.997532	Jeff	2	Jeff	20000.00	1
568	opex	purchase coffee blender	2024-02-12 12:09:11.643331	Jeff	2	Jeff	10000.00	1
569	opex	opex	2024-02-13 08:33:53.88716	Jeff	2	Jeff	20000.00	1
570	opex	opex	2024-02-15 10:30:00.583365	Jeff	2	Jeff	20000.00	1
571	internet	internet sub	2024-02-15 10:30:33.466595	Jeff	2	Jeff	25000.00	1
572	opex	opex and fuel	2024-02-18 09:20:11.224909	Jeff	2	Jeff	45000.00	1
573	opex	opex	2024-02-22 18:08:26.774906	Jeff	2	Jeff	20000.00	1
574	opex	payment for customer clearance	2024-02-24 09:07:24.097047	De Youhance Agent	2	Jeff	249600.00	1
575	opex	opex	2024-02-29 18:54:20.850416	Jeff	2	Jeff	10000.00	1
576	opex	paid accountant for book filing	2024-03-01 19:41:17.291524	Jeff	2	Jeff	50000.00	1
577	opex	opex	2024-03-01 19:42:07.711458	Jeff	2	Jeff	20000.00	1
578	electrcial recharge	ikedc recharge	2024-03-02 17:19:27.188548	Jeff	2	Jeff	10000.00	1
579	opex	opex	2024-03-06 16:23:11.208338	Jeff	2	Jeff	65000.00	1
580	instalation charges	tracker installation charges	2024-03-07 09:39:07.08571	Engr	2	Jeff	10000.00	1
581	referral bonus	paid referral bonus 	2024-03-07 09:40:13.463174	Tess	2	Jeff	5000.00	1
582	opex	opex	2024-03-07 14:29:23.323792	Jeff	2	Jeff	20000.00	1
583	electrical fixes	electrical fixes	2024-03-07 14:29:50.513822	Jeff	2	Jeff	12000.00	1
584	internet sub	internet subscription	2024-03-15 14:53:12.230002	Jeff	2	Jeff	22000.00	1
585	opex	opex	2024-03-15 17:53:44.629401	Jeff	2	Jeff	25000.00	1
586	opex	opex	2024-03-16 18:23:25.628088	Jeff	2	Jeff	40000.00	1
587	opex	opex	2024-03-18 09:29:39.057917	Jeff	2	Jeff	20000.00	1
588	fb ads	fb ads	2024-03-18 09:29:57.20682	Jeff	2	Jeff	60000.00	1
589	opex	car battery purchase	2024-03-21 09:25:29.483688	Jeff	2	Jeff	35000.00	1
590	miscellenous	miscellenous	2024-03-25 19:46:46.310194	Jeff	2	Jeff	75000.00	4
591	drawings	drawings	2024-03-30 08:33:50.557142	Jeff	2	Jeff	50000.00	1
592	opex	opex	2024-03-31 12:57:33.939889	jeff	2	Jeff	20000.00	1
593	shipment fee	payment for shipment	2024-04-04 09:37:06.079903	De Youhance shipment	2	Jeff	29400.00	1
594	opex	opex exp	2024-04-11 17:11:19.30903	Jeff	2	Jeff	62000.00	1
595	usd purchase	usd purchase for ads	2024-04-26 07:41:39.11036	Jeff	2	Jeff	45000.00	1
596	account filing balance	account filing balance 	2024-04-26 08:06:30.614351	Taiwo	2	Jeff	25000.00	1
597	opex	opex	2024-04-26 08:06:53.314141	Jeff	2	Jeff	41500.00	1
598	rent part payment	rent part payment	2024-04-26 08:07:25.596337	Jeff	2	Jeff	300000.00	1
599	loan repayment	loan repayment	2024-04-26 08:07:52.734128	Choma	2	Jeff	168000.00	1
600	opex	opex	2024-04-26 08:08:16.479741	jeff	2	jeff	100000.00	1
601	opex	opex	2024-04-26 08:09:28.475547	jeff	2	jeff	150000.00	1
602	loan repayment	loan repayment	2024-04-26 08:10:20.695988	Chioma	2	Jeff	35000.00	1
603	car fixes	car fixes	2024-04-26 08:12:26.245096	Jeff	2	jeff	20000.00	1
604	contractor engagement	contractor engagement part payment	2024-04-26 08:13:04.268451	Omotayo	2	jeff	100000.00	1
605	opex	opex	2024-04-26 10:08:20.879964	Jeff	2	jeff	40000.00	1
606	opex and delivery	opex and delivery	2024-04-29 09:05:26.281805	jeff	2	Jeff	20000.00	1
607	opex	opex	2024-05-01 20:03:23.616587	Jeff	2	Jeff	15000.00	1
608	opex	opex	2024-05-02 12:37:44.800376	jeff	2	Jeff	50000.00	1
609	opex	opex	2024-05-07 06:45:03.01771	Jeff	2	jeff	30000.00	1
610	opex	opex	2024-05-14 08:41:13.4288	Jeff	2	jeff	20000.00	1
611	usd procurement	usd procurement	2024-05-16 19:02:44.108692	Mobifin server	2	jeff	156000.00	1
613	opex	opex	2024-05-20 13:08:33.284645	Jeff	2	Jeff	40000.00	1
614	Contractor payment	second installation 	2024-05-20 13:08:57.055669	Omash	2	Jeff	50000.00	1
612	exp	exp	2024-05-17 22:23:02.682735	jeff	2	jeff	40000.00	1
615	opex	opex	2024-05-21 09:22:07.700892	Jeff	2	Jeff	20000.00	1
616	opex	opex	2024-05-22 12:25:20.762225	Jeff	2	jeff	31000.00	1
617	Contractor Payment	contractor balance payment	2024-05-23 10:53:09.580876	Jeff	2	Jeff	50000.00	1
618	opex	opex	2024-05-29 11:50:18.760433	Jeff	2	Jeff	35000.00	1
619	opex	opex	2024-05-30 16:24:11.854172	Jeff	2	Jeff	20000.00	1
620	opex	opex	2024-05-31 21:31:44.328941	Jeff	2	Jeff	32000.00	1
621	opex	opex	2024-06-18 16:21:28.216019	jeff	2	JEff	20000.00	1
622	opex	gen repairs	2024-06-19 12:50:32.399992	Jeff	2	Jeff	20000.00	1
623	opex	opex	2024-06-23 08:40:36.667347	Jeff	2	Jeff	50000.00	1
624	opex	opex andl oan repayment	2024-06-26 09:23:28.488848	Jeff	2	Jeff	45000.00	1
625	opex	opex	2024-06-28 06:51:39.934512	Jeff	2	Jeff	20000.00	1
626	opex	internet and electric and repairs	2024-06-29 09:47:26.060718	Jeff	2	Jeff	40000.00	1
627	opex	opex	2024-07-04 11:03:13.919739	Jeff	2	Jeff	28000.00	1
628	opex	opex	2024-07-10 21:17:40.710093	Jeff	2	Jeff	15000.00	1
629	opex	opex	2024-07-12 13:49:03.340149	jeff	2	Jeff	15000.00	1
630	opex	opex	2024-07-15 08:32:59.501471	Jeff	2	Jeff	20000.00	1
631	opex	opex	2024-07-17 15:11:35.507911	jeff	2	Jeff	20000.00	1
632	opex	car fix and servicing	2024-07-18 08:19:37.540421	jeff	2	Jeff	36000.00	1
633	opex	opex and relocation exp	2024-07-30 20:43:18.719802	jeff	2	Jeff	250000.00	1
634	opex	opex	2024-07-31 08:48:29.912736	jeff	2	Jeff	15000.00	1
635	opex	opex for the helper	2024-07-31 18:21:39.998406	Jeff	2	Jeff	40000.00	1
636	opex	opex	2024-08-01 18:55:40.608606	jeff	2	jeff	20000.00	1
637	opex	opex for repairs and installation	2024-08-03 22:36:11.900478	jeff	2	jeff	80000.00	1
638	opex 	opex for fuel exp	2024-08-06 12:21:23.55687	Jeff	2	Jeff	40000.00	1
639	opex	opex and fuel purchase	2024-08-07 19:30:02.342219	Jeff	2	Jeff	15000.00	1
642	license renewal	drivers license renewal	2024-08-15 10:52:00.789348	Jeff	2	Jeff	50000.00	1
643	opex	opex	2024-08-16 16:34:09.662756	Jeff	2	Jeff	10000.00	1
644	opex 	opex	2024-08-18 14:44:58.587726	Jeff	2	Jeff	20000.00	1
645	opex	opex	2024-08-19 10:58:38.11163	Jeff	2	Jeff	23000.00	1
646	opex	fuel purchase	2024-08-22 09:00:10.433249	Jeff	2	Jeff	10000.00	1
647	opex	opex	2024-08-22 09:00:28.109837	Jeff	2	Jeff	20000.00	1
648	opex	opex	2024-08-23 09:30:53.503046	Jeff	2	Jeff	20000.00	1
649	domain renewal	domain renewal ecardex.com	2024-08-26 09:53:44.920619	Jeff	2	Jeff	28800.00	1
650	opex	opex	2024-08-29 08:44:49.52031	Jeff	2	Jeff	80000.00	1
651	opex	opex for miscellenous	2024-08-30 18:55:18.699842	Jeff	2	Jeff	50000.00	1
652	opex	opex	2024-09-02 10:26:48.818996	Jeff	2	Jeff	33000.00	1
653	opex	opex	2024-09-07 08:23:16.528006	Jeff	2	Jeff	22600.00	1
\.


--
-- Data for Name: invoice; Type: TABLE DATA; Schema: public; Owner: sysdba
--

COPY public.invoice (id, disc_type, disc_value, purchase_no, invoice_no, date_value, invoice_due, client_type, currency, client_id, disc_desc, is_dummy) FROM stdin;
1	\N	\N	1	INV-1	2019-12-20 11:13:58.244104	2019-12-20 11:13:58.244117	3	1	1	\N	\N
2	\N	\N	2	INV-2	2019-12-23 11:55:22.290145	2019-12-23 11:55:22.290158	1	1	2	\N	\N
3	\N	\N	3	INV-3	2020-01-11 13:20:53.295471	2020-01-11 13:20:53.295491	1	1	3	\N	\N
4	\N	\N	4	INV-4	2020-01-14 21:59:28.287614	2020-01-14 21:59:28.287635	1	1	4	\N	\N
5	fixed	11000.00	5	INV-5	2020-02-25 12:13:11.331516	2020-02-25 12:13:11.331527	3	1	5	\N	\N
6	\N	\N	6	INV-6	2020-03-06 22:19:02.95531	2020-03-06 22:19:02.95532	1	1	6	\N	\N
7	\N	\N	7	INV-7	2020-03-07 14:17:03.860753	2020-03-07 14:17:03.860769	1	1	7	\N	\N
8	fixed	7000.00	8	INV-8	2020-03-11 10:06:02.168736	2020-03-11 10:06:02.168745	3	1	8	\N	\N
9	\N	\N	9	INV-9	2020-03-17 12:19:19.995316	2020-03-17 12:19:19.995327	3	1	9	\N	\N
42	\N	\N	42	INV-42	2021-04-07 09:04:34.224143	2021-04-07 09:04:34.224153	1	1	24	\N	\N
11	\N	\N	11	INV-11	2020-04-21 18:20:48.309266	2020-04-21 18:20:48.309276	1	1	11	\N	\N
12	\N	\N	12	INV-12	2020-04-24 16:04:40.104619	2020-04-24 16:04:40.104628	2	1	12	\N	\N
10	\N	\N	10	INV-10	2020-04-15 15:44:13.262891	2020-04-15 15:44:13.2629	3	1	10	\N	\N
43	\N	\N	43	INV-43	2021-04-07 09:05:54.817927	2021-04-07 09:05:54.817936	3	1	14	\N	\N
13	fixed	2500.00	13	INV-13	2020-06-29 15:12:28.417347	2020-06-29 15:12:28.417356	2	1	13	One month free	\N
14	\N	\N	14	INV-14	2020-07-13 09:36:38.221239	2020-07-13 09:36:38.221248	2	1	14	\N	\N
15	\N	\N	15	INV-15	2020-07-17 11:50:27.082596	2020-07-17 11:50:27.082606	3	1	15	\N	\N
16	fixed	2000.00	16	INV-16	2020-08-11 10:57:32.038254	2020-08-11 10:57:32.038271	3	1	16	discount	\N
44	\N	\N	44	INV-44	2021-04-09 12:39:01.348264	2021-04-09 12:39:01.348281	1	1	24	\N	\N
17	\N	\N	17	INV-17	2020-09-28 15:46:58.140419	2020-09-28 15:46:58.140428	1	1	17	\N	\N
18	\N	\N	18	INV-18	2020-10-01 17:10:24.46641	2020-10-01 17:10:24.466425	2	1	18	\N	\N
19	\N	\N	19	INV-19	2020-11-05 19:05:54.02696	2020-11-05 19:05:54.026968	1	1	18	\N	\N
20	\N	\N	20	INV-20	2020-12-10 16:44:46.533252	2020-12-10 16:44:46.53326	3	1	10	\N	\N
21	\N	\N	21	INV-21	2020-12-15 14:11:10.496769	2020-12-15 14:11:10.496777	3	1	19	\N	\N
22	\N	\N	22	INV-22	2021-01-18 09:52:22.716216	2021-01-18 09:52:22.716225	3	1	16	\N	\N
45	\N	\N	45	INV-45	2021-04-09 12:39:52.214886	2021-04-09 12:39:52.214895	1	1	24	\N	\N
23	fixed	7000.00	23	INV-23	2021-01-25 16:18:43.718508	2021-01-25 16:18:43.718518	3	1	20	additional discount	\N
24	\N	\N	24	INV-24	2021-01-29 10:30:27.956973	2021-01-29 10:30:27.956982	3	1	21	\N	\N
25	\N	\N	25	INV-25	2021-02-04 11:59:28.493829	2021-02-04 11:59:28.493842	2	1	18	\N	\N
26	fixed	262.50	26	INV-26	2021-02-09 10:34:00.599226	2021-02-09 10:34:00.599241	3	1	18	vat absorbed	\N
46	\N	\N	46	INV-46	2021-04-09 12:40:26.409397	2021-04-09 12:40:26.409412	1	1	24	\N	\N
27	percent	0.00	27	INV-27	2021-02-13 09:29:23.390158	2021-02-13 09:29:23.390167	3	1	16		\N
28	\N	\N	28	INV-28	2021-03-01 13:56:37.067614	2021-03-01 13:56:37.067624	2	1	21	\N	\N
29	\N	\N	29	INV-29	2021-03-01 13:57:39.528353	2021-03-01 13:57:39.528361	2	1	20	\N	\N
30	\N	\N	30	INV-30	2021-03-03 14:03:13.338146	2021-03-03 14:03:13.338155	3	1	22	\N	\N
31	\N	\N	31	INV-31	2021-03-05 10:38:54.86062	2021-03-05 10:38:54.860629	2	1	23	\N	\N
32	\N	\N	32	INV-32	2021-03-05 16:16:45.481533	2021-03-05 16:16:45.481544	1	1	24	\N	\N
33	\N	\N	33	INV-33	2021-03-05 16:17:57.53893	2021-03-05 16:17:57.538939	1	1	24	\N	\N
34	\N	\N	34	INV-34	2021-03-08 10:47:31.928356	2021-03-08 10:47:31.928369	1	1	24	\N	\N
35	\N	\N	35	INV-35	2021-03-08 10:57:32.726803	2021-03-08 10:57:32.726812	1	1	24	\N	\N
36	\N	\N	36	INV-36	2021-03-11 19:32:49.538856	2021-03-11 19:32:49.538871	1	1	25	\N	\N
37	\N	\N	37	INV-37	2021-03-18 17:12:20.981988	2021-03-18 17:12:20.982002	1	1	24	\N	\N
38	\N	\N	38	INV-38	2021-03-28 10:11:08.351131	2021-03-28 10:11:08.351141	1	1	24	\N	\N
39	\N	\N	39	INV-39	2021-03-29 09:58:37.962426	2021-03-29 09:58:37.962435	3	1	16	\N	\N
40	\N	\N	40	INV-40	2021-04-05 08:40:32.166282	2021-04-05 08:40:32.166292	2	1	23	\N	\N
41	\N	\N	41	INV-41	2021-04-05 14:14:11.378825	2021-04-05 14:14:11.378835	1	1	24	\N	\N
47	\N	\N	47	INV-47	2021-04-11 09:59:52.064989	2021-04-11 09:59:52.064998	3	1	26	\N	\N
48	\N	\N	48	INV-48	2021-04-12 00:12:23.632209	2021-04-12 00:12:23.632222	1	1	24	\N	\N
49	\N	\N	49	INV-49	2021-04-18 12:42:14.164583	2021-04-18 12:42:14.164598	1	1	24	\N	\N
50	\N	\N	50	INV-50	2021-04-20 11:41:02.761547	2021-04-20 11:41:02.761556	1	1	24	\N	\N
51	\N	\N	51	INV-51	2021-04-22 07:30:07.916284	2021-04-22 07:30:07.916293	1	1	24	\N	\N
52	\N	\N	52	INV-52	2021-04-22 14:40:16.6518	2021-04-22 14:40:16.651817	1	1	24	\N	\N
53	\N	\N	53	INV-53	2021-04-23 09:13:03.89748	2021-04-23 09:13:03.897494	1	1	24	\N	\N
61	\N	\N	61	INV-61	2021-06-22 09:58:10.4666	2021-06-22 09:58:10.466611	2	1	28	\N	\N
55	\N	\N	55	INV-55	2021-04-26 15:35:02.826842	2021-04-26 15:35:02.826852	3	1	13	\N	\N
56	\N	\N	56	INV-56	2021-04-27 19:32:04.411574	2021-04-27 19:32:04.411602	1	1	24	\N	\N
57	\N	\N	57	INV-57	2021-04-29 14:31:15.139391	2021-04-29 14:31:15.1394	2	1	27	\N	\N
58	\N	\N	58	INV-58	2021-04-30 10:34:00.292605	2021-04-30 10:34:00.29262	1	1	18	\N	\N
59	\N	\N	59	INV-59	2021-05-10 19:34:58.006702	2021-05-10 19:34:58.006711	1	1	23	\N	\N
60	\N	\N	60	INV-60	2021-05-10 19:53:06.066514	2021-05-10 19:53:06.066523	3	1	10	\N	\N
54	fixed	1500.00	54	INV-54	2021-04-26 15:27:02.223118	2021-04-26 15:27:02.223127	2	1	16	discount on the trackers	\N
62	\N	\N	62	INV-62	2021-06-28 18:28:21.011889	2021-06-28 18:28:21.011898	2	1	22	\N	\N
63	\N	\N	63	INV-63	2021-07-04 20:24:06.151483	2021-07-04 20:24:06.151492	1	1	24	\N	\N
64	\N	\N	64	INV-64	2021-07-05 14:32:45.651408	2021-07-05 14:32:45.651417	1	1	24	\N	\N
65	\N	\N	65	INV-65	2021-07-05 19:57:30.009003	2021-07-05 19:57:30.009012	1	1	24	\N	\N
66	\N	\N	66	INV-66	2021-07-12 07:52:15.113124	2021-07-12 07:52:15.113133	1	1	24	\N	\N
67	\N	\N	67	INV-67	2021-07-12 07:53:05.090286	2021-07-12 07:53:05.090294	1	1	24	\N	\N
68	\N	\N	68	INV-68	2021-07-12 08:42:39.882044	2021-07-12 08:42:39.882052	1	1	24	\N	\N
69	\N	\N	69	INV-69	2021-07-12 08:43:45.401795	2021-07-12 08:43:45.401804	1	1	24	\N	\N
70	\N	\N	70	INV-70	2021-07-14 19:31:32.608678	2021-07-14 19:31:32.6087	1	1	24	\N	\N
71	\N	\N	71	INV-71	2021-07-17 09:43:24.181049	2021-07-17 09:43:24.181058	1	1	24	\N	\N
72	\N	\N	72	INV-72	2021-07-17 09:43:53.139523	2021-07-17 09:43:53.139532	1	1	24	\N	\N
73	\N	\N	73	INV-73	2021-07-17 12:08:15.525406	2021-07-17 12:08:15.525416	2	1	14	\N	\N
74	\N	\N	74	INV-74	2021-07-23 13:51:48.067612	2021-07-23 13:51:48.067621	1	1	24	\N	\N
75	\N	\N	75	INV-75	2021-07-27 09:33:30.49736	2021-07-27 09:33:30.497369	1	1	24	\N	\N
77	\N	\N	77	INV-77	2021-07-30 18:23:13.938959	2021-07-30 18:23:13.938967	1	1	29	\N	\N
76	fixed	500.00	76	INV-76	2021-07-27 09:34:19.883963	2021-07-27 09:34:19.883978	1	1	24		\N
78	\N	\N	78	INV-78	2021-08-02 19:18:19.840168	2021-08-02 19:18:19.840177	3	1	30	\N	\N
79	\N	\N	79	INV-79	2021-08-05 10:52:12.443646	2021-08-05 10:52:12.443656	3	1	26	\N	\N
80	\N	\N	80	INV-80	2021-08-09 08:35:42.753338	2021-08-09 08:35:42.753348	1	1	31	\N	\N
81	\N	\N	81	INV-81	2021-09-24 10:17:47.771115	2021-09-24 10:17:47.771129	3	1	16	\N	\N
82	\N	\N	82	INV-82	2021-10-01 08:58:19.03223	2021-10-01 08:58:19.032242	3	1	16	\N	\N
83	\N	\N	83	INV-83	2021-10-01 09:45:57.161991	2021-10-01 09:45:57.162009	1	1	24	\N	\N
85	\N	\N	85	INV-85	2021-10-04 19:26:44.076798	2021-10-04 19:26:44.076807	3	1	26	\N	\N
84	\N	\N	84	INV-84	2021-10-04 16:03:38.437593	2021-10-04 16:03:38.437602	3	1	26	\N	\N
87	\N	\N	87	INV-87	2021-11-01 06:57:01.820319	2021-11-01 06:57:01.820334	3	1	32	\N	\N
121	\N	\N	121	INV-121	2023-06-21 09:27:59.042045	2023-06-21 09:27:59.04206	1	1	16	\N	\N
88	fixed	5400.00	88	INV-88	2021-11-12 15:37:32.617577	2021-11-12 15:37:32.617588	3	1	10	no vat	\N
122	\N	\N	122	INV-122	2023-06-30 15:24:24.712298	2023-06-30 15:24:24.712306	1	1	24	\N	\N
123	\N	\N	123	INV-123	2023-07-12 10:55:30.876497	2023-07-12 10:55:30.876526	1	1	48	\N	\N
89	\N	\N	89	INV-89	2021-11-12 15:56:23.121569	2021-11-12 15:56:23.121578	1	1	33	\N	\N
124	\N	\N	124	INV-124	2023-07-31 21:01:26.988017	2023-07-31 21:01:26.988059	1	1	24	\N	\N
90	\N	\N	90	INV-90	2021-10-31 12:35:31.728901	2021-10-31 12:35:31.728901	1	1	24	\N	\N
91	\N	\N	91	INV-91	2021-12-04 11:20:17.994487	2021-12-04 11:20:17.994496	1	1	24	\N	\N
92	\N	\N	92	INV-92	2021-12-13 21:50:42.202679	2021-12-13 21:50:42.202688	1	1	24	\N	\N
93	\N	\N	93	INV-93	2022-01-14 17:40:12.239389	2022-01-14 17:40:12.239398	1	1	24	\N	\N
94	\N	\N	94	INV-94	2022-01-24 15:47:02.165695	2022-01-24 15:47:02.165704	1	1	34	\N	\N
95	fixed	20000.00	95	INV-95	2022-01-25 12:41:50.128052	2022-01-25 12:41:50.128061	1	1	35	installation charge discount	\N
125	\N	\N	125	INV-125	2023-08-31 09:04:08.613788	2023-08-31 09:04:08.613808	1	1	24	\N	\N
96	fixed	6000.00	96	INV-96	2022-01-31 12:05:01.197036	2022-01-31 12:05:01.197046	1	1	36	discount	\N
97	\N	\N	97	INV-97	2022-03-13 22:29:39.67695	2022-03-13 22:29:39.676959	1	1	37	\N	\N
98	\N	\N	98	INV-98	2022-03-16 18:40:52.396586	2022-03-16 18:40:52.396602	1	1	38	\N	\N
99	\N	\N	99	INV-99	2022-03-21 15:26:32.148931	2022-03-21 15:26:32.14894	1	1	39	\N	\N
100	\N	\N	100	INV-100	2022-04-05 09:39:53.872602	2022-04-05 09:39:53.872611	3	1	16	\N	\N
101	\N	\N	101	INV-101	2022-04-28 16:21:38.440065	2022-04-28 16:21:38.440074	1	1	16	\N	\N
102	\N	\N	102	INV-102	2022-05-09 09:05:45.508031	2022-05-09 09:05:45.508047	1	1	10	\N	\N
103	\N	\N	103	INV-103	2022-05-13 15:04:38.787989	2022-05-13 15:04:38.788009	3	1	40	\N	\N
104	\N	\N	104	INV-104	2022-05-20 11:24:32.080006	2022-05-20 11:24:32.080015	3	1	10	\N	\N
105	\N	\N	105	INV-105	2022-10-18 10:53:28.3128	2022-10-18 10:53:28.31281	1	1	41	\N	\N
106	\N	\N	106	INV-106	2022-11-22 08:26:57.736302	2022-11-22 08:26:57.736313	1	1	42	\N	\N
107	\N	\N	107	INV-107	2022-11-28 12:08:22.515969	2022-11-28 12:08:22.515978	1	1	10	\N	\N
108	\N	\N	108	INV-108	2023-01-26 11:41:41.691563	2023-01-26 11:41:41.691571	1	1	43	\N	\N
109	\N	\N	109	INV-109	2023-01-31 18:18:47.1187	2023-01-31 18:18:47.118708	1	1	24	\N	\N
126	\N	\N	126	INV-126	2023-09-15 14:23:20.735646	2023-09-15 14:23:20.735668	1	1	34	\N	\N
110	\N	\N	110	INV-110	2023-02-27 08:42:19.352201	2023-02-27 08:42:19.352201	1	1	24	\N	\N
111	\N	\N	111	INV-111	2023-03-14 10:03:57.541591	2023-03-14 10:03:57.541603	1	1	34	\N	\N
112	\N	\N	112	INV-112	2023-03-25 23:08:36.294316	2023-03-25 23:08:36.294329	1	1	44	\N	\N
113	\N	\N	113	INV-113	2023-03-31 09:54:12.127115	2023-03-31 09:54:12.127122	1	1	45	\N	\N
142	\N	\N	142	INV-142	2024-03-22 13:33:16.602784	2024-03-22 13:33:16.602797	1	1	53	\N	\N
127	\N	\N	127	INV-127	2023-09-30 02:57:55.28924	2023-09-30 02:57:55.28924	1	1	24	\N	\N
115	\N	\N	115	INV-115	2023-03-31 12:32:59.150505	2023-03-31 12:32:59.150513	1	1	14	\N	\N
116	\N	\N	116	INV-116	2023-03-31 21:33:03.202309	2023-03-31 21:33:03.202309	1	1	24	\N	\N
128	\N	\N	128	INV-128	2023-11-08 07:30:55.922731	2023-11-08 07:30:55.922739	1	1	34	\N	\N
117	\N	\N	117	INV-117	2023-04-30 08:48:53.011751	2023-04-30 08:48:53.011751	1	1	24	\N	\N
118	\N	\N	118	INV-118	2023-05-15 15:02:51.244432	2023-05-15 15:02:51.244442	1	1	10	\N	\N
114	\N	\N	114	INV-114	2023-03-31 10:09:16.72946	2023-03-31 10:09:16.729467	1	1	47	\N	1
119	\N	\N	119	INV-119	2023-05-23 13:59:34.036877	2023-05-23 13:59:34.036888	1	1	48	\N	\N
120	\N	\N	120	INV-120	2023-05-30 19:35:26.854404	2023-05-30 19:35:26.854411	1	1	24	\N	\N
129	\N	\N	129	INV-129	2023-11-15 10:51:53.484654	2023-11-15 10:51:53.484667	1	1	10	\N	\N
130	\N	\N	130	INV-130	2023-11-22 08:01:58.780796	2023-11-22 08:01:58.780807	1	1	49	\N	\N
131	\N	\N	131	INV-131	2023-11-30 18:20:02.375454	2023-11-30 18:20:02.375454	1	1	24	\N	\N
132	\N	\N	132	INV-132	2023-12-12 11:12:23.759882	2023-12-12 11:12:23.75989	1	1	50	\N	\N
133	\N	\N	133	INV-133	2023-12-14 14:51:00.017388	2023-12-14 14:51:00.0174	1	1	51	\N	\N
143	\N	\N	143	INV-143	2024-03-27 17:17:38.870099	2024-03-27 17:17:38.870118	1	1	34	\N	\N
134	\N	\N	134	INV-134	2023-12-31 10:21:20.527225	2023-12-31 10:21:20.527225	1	1	24	\N	\N
135	\N	\N	135	INV-135	2024-01-10 12:28:49.991229	2024-01-10 12:28:49.991239	1	1	34	\N	\N
136	\N	\N	136	INV-136	2024-01-10 12:30:03.869564	2024-01-10 12:30:03.869578	1	1	34	\N	\N
137	\N	\N	137	INV-137	2024-01-14 11:41:42.41313	2024-01-14 11:41:42.41314	1	1	47	\N	\N
138	\N	\N	138	INV-138	2024-01-23 18:36:34.960733	2024-01-23 18:36:34.960741	1	1	33	\N	\N
139	\N	\N	139	INV-139	2024-01-30 14:45:34.671353	2024-01-30 14:45:34.671353	1	1	24	\N	\N
144	\N	\N	144	INV-144	2024-04-01 08:38:40.817435	2024-04-01 08:38:40.817449	1	1	24	\N	\N
140	\N	\N	140	INV-140	2024-02-29 12:53:23.701643	2024-02-29 12:53:23.701643	1	1	24	\N	\N
141	\N	\N	141	INV-141	2024-03-07 08:41:31.70479	2024-03-07 08:41:31.704807	1	1	52	\N	\N
145	\N	\N	145	INV-145	2024-04-26 08:22:44.852348	2024-04-26 08:22:44.852357	1	1	24	\N	\N
153	\N	\N	153	INV-153	2024-07-05 12:19:52.392864	2024-07-05 12:19:52.392875	1	1	55	\N	\N
147	\N	\N	147	INV-147	2024-05-04 21:57:40.321706	2024-05-04 21:57:40.321716	1	1	34	\N	\N
148	\N	\N	148	INV-148	2024-05-06 08:20:16.744641	2024-05-06 08:20:16.744651	1	1	10	\N	\N
149	\N	\N	149	INV-149	2024-05-07 15:17:10.084267	2024-05-07 15:17:10.084278	1	1	54	\N	\N
150	\N	\N	150	INV-150	2024-05-23 09:18:25.578051	2024-05-23 09:18:25.57806	1	1	54	\N	\N
146	fixed	10000.00	146	INV-146	2024-05-04 21:56:46.282555	2024-05-04 21:56:46.28257	1	1	34	discount applied	\N
151	\N	\N	151	INV-151	2024-05-30 09:00:55.009204	2024-05-30 09:00:55.009214	1	1	24	\N	\N
152	\N	\N	152	INV-152	2024-06-30 04:48:18.995831	2024-06-30 04:48:18.995839	1	1	24	\N	\N
154	\N	\N	154	INV-154	2024-07-24 23:30:15.453533	2024-07-24 23:30:15.453547	1	1	34	\N	\N
155	\N	\N	155	INV-155	2024-07-30 20:39:58.32712	2024-07-30 20:39:58.327127	1	1	24	\N	\N
156	\N	\N	156	INV-156	2024-08-12 12:14:24.91958	2024-08-12 12:14:24.919599	1	1	54	\N	\N
157	\N	\N	157	INV-157	2024-08-21 15:39:58.170254	2024-08-21 15:39:58.170263	1	1	34	\N	\N
\.


--
-- Data for Name: item; Type: TABLE DATA; Schema: public; Owner: sysdba
--

COPY public.item (id, item_desc, qty, rate, amount, invoice_id) FROM stdin;
1	Mobile application development for VAS. With workflow enabled processes	1	1200000	1200000.00	1
2	Mobile UI mockup design 	1	20000	20000.00	1
3	Data Science For Beginners	1	65000	65000.00	2
4	Datascience For Beginners -- January Session	1	65000	65000.00	3
5	Personal Python Class	1	100000	100000.00	4
6	Payment for Tracking devices	2	13500	27000.00	5
7	Installation Fee	2	2000	4000.00	5
8	Subscription Fee One month	2	3500	7000.00	5
9	Registration for Datascience	1	10000	10000.00	6
10	Balance payment for Datascience	1	55000	55000.00	6
11	Registration Fee for Javascript class	1	10000	10000.00	7
12	Balance fee for Javascript training	1	30000	30000.00	7
13	Tracking devices	2	13500	27000.00	8
14	Installation Fee	2	2500	5000.00	8
15	Bike 01 Subscription fee for 1 year	12	3500	42000.00	8
16	Bike 02 Subscription fee for one year	12	3500	42000.00	8
18	Tracker Devices	7	13500	94500.00	9
19	Installation Fee	7	1500	10500.00	9
60	Tracker Installation	1	3000	3000.00	25
23	Integration with Mobifin Platform	1	40000	40000.00	10
62	one month subsctiption	1	3500	3500.00	26
63	subscription renewal for six months	3	15000	45000.00	27
24	Cash injection to the business	1	330000	330000.00	11
25	Developmental fee for Invoicing application	1	350000	350000.00	12
26	Developmental fee for admin mgt portal for the invoicing portal	1	350000	350000.00	12
27	Capricon Digitals Integration (All Services)	1	350000	350000.00	10
28	Deployment and Server Security Setup	1	50000	50000.00	10
29	Linux Cloud Server  Setup	12	7000	84000.00	10
30	Track device 	1	15000	15000.00	13
32	Track installation	1	2500	2500.00	13
83	Subscription renewal	1	3500	3500.00	40
31	Maptrack subscription	12	2500	30000.00	13
33	Tracker Device	1	16000	16000.00	14
34	Tracker installation	1	3000	3000.00	14
35	subscription plan	3	3000	9000.00	14
36	Payment Platform Development and Deployment For\r\n6 Months Engagements	1	4500000	4500000.00	15
37	Tracker Device Purchase	2	16000	32000.00	16
38	Installation Fee	2	3000	6000.00	16
39	6 months Subscription for two devices	6	5000	30000.00	16
64	subscription	2	3500	7000.00	25
65	maptrackapp subscription	1	3500	3500.00	28
66	subscription for March 	5	2500	12500.00	29
67	Tracker device	2	14500	29000.00	30
40	Software Rework  for audio fingerprint matching. 	1	380000	380000.00	17
41	tracker device cost	1	16000	16000.00	18
42	installation fee	1	3000	3000.00	18
68	tracker installation	2	3000	6000.00	30
69	tracker device	1	16000	16000.00	31
43	subscription	1	3500	3500.00	18
44	Payment for maptrack subsctiption	1	3500	3500.00	19
45	Admin Stats Rework	1	85000	85000.00	20
46	Tracking device	1	16000	16000.00	21
47	subscription for 6months	6	2500	15000.00	21
48	Tracker Installation fee	1	3000	3000.00	21
50	One month subscription	1	2500	2500.00	22
51	Tracker installation	1	3000	3000.00	22
49	Tracker device 	1	16000	16000.00	22
52	Tracker device replacement	1	10000	10000.00	22
53	Trackers for maptrack app	5	16000	80000.00	23
54	tracker installation	5	3000	15000.00	23
55	One month subscription	5	3500	17500.00	23
56	tracker device	1	16000	16000.00	24
57	tracker Installation	1	3000	3000.00	24
58	One month subscription	1	3500	3500.00	24
59	Tracker Device	1	16000	16000.00	25
70	tracker installation fee	1	3000	3000.00	31
71	one month subscription	1	3500	3500.00	31
72	Purchase of laptop stand	1	12000	12000.00	32
73	delivery fee	1	2000	2000.00	32
74	Infrared thermometer	1	7000	7000.00	33
76	laptop stand 	1	14000	14000.00	34
77	bed tray Table stand 	2	12000	24000.00	35
78	Aiqura  Infrared Forehead Thermometer	6	5500	33000.00	36
79	fitbit wrist watch	2	3500	7000.00	37
80	Fit Pro watch	1	4000	4000.00	38
84	Slim laptop bag , Black	1	6000	6000.00	41
81	tracker device	2	16000	32000.00	39
82	subscription for 5 months for two trackers	10	2500	25000.00	39
85	Laptop bag	1	6500	6500.00	42
86	Payment for tracker	1	16000	16000.00	43
87	subscription for two trackers quarterly	2	9000	18000.00	43
88	tracker installation	1	4000	4000.00	43
89	laptop stand with cooling fan	1	15000	15000.00	44
90	laptop bag - color black	1	6500	6500.00	45
91	Laptop Bag - color Black	1	6500	6500.00	46
92	tracker devices	5	16000	80000.00	47
94	laptop bag	1	6500	6500.00	48
95	Laptop bag	4	6500	26000.00	49
96	purchase of table tray	1	10000	10000.00	50
93	annual subscription	5	2500	12500.00	47
97	laptop bag, blue color	1	6500	6500.00	51
98	laptop bag	1	6500	6500.00	52
99	power bank 10000 mah	1	6000	6000.00	53
100	tracker device replacement	1	16000	16000.00	54
101	Tracker device replacement 	1	16000	16000.00	55
102	laptop bag gray color	1	6000	6000.00	56
103	Tracker device 	1	16000	16000.00	57
104	subscription for 1 month	1	3500	3500.00	57
105	tracking subscription renewal	1	3500	3500.00	58
106	Payment for tracker subscription	12	2500	30000.00	59
108	Server maintenance fee	1	30000	30000.00	60
107	server hosting cost (NGN)	6	10000	60000.00	60
109	new tracker devices	2	16000	32000.00	54
110	subscription for three months on two trackers	6	2500	15000.00	54
111	installation fee for two bikes	2	3500	7000.00	54
112	Backend Project Implementation 	1	500000	500000.00	61
113	subscription for 7 months for two bikes	14	2500	35000.00	62
114	Purchase of laptop bag	1	9000	9000.00	63
115	purchase of laptop bag	1	9000	9000.00	64
116	laptop bag	1	9000	9000.00	65
117	Black laptop bag	1	9000	9000.00	66
118	Gray laptop bag	1	8000	8000.00	67
119	Laptop bag 	1	9000	9000.00	68
120	delivery fee	1	2500	2500.00	68
121	Laptop bag, blue color	1	9000	9000.00	69
122	Laptop bag black	1	9000	9000.00	70
123	fitbit watch	2	3500	7000.00	70
124	laptop bag purchase	2	9000	18000.00	71
125	laptop bag black color	1	9000	9000.00	72
126	subscription payment for maptrackapp	2	3500	7000.00	73
127	laptop bag color blue	1	9000	9000.00	74
128	laptop bag blue color	1	8500	8500.00	75
129	laptop bag black color 	1	9000	9000.00	76
130	Python class for web developmnt	1	90000	90000.00	77
131	tracker devices	18	16000	288000.00	78
132	annual subscription fee	18	26000	468000.00	78
133	installation fee	18	4000	72000.00	78
134	Tracker subscription for two vehicles	3	5000	15000.00	79
135	python backend training online	1	60000	60000.00	80
136	frontend javascript, html and css class	1	60000	60000.00	80
137	reactjs and react native for mobile development	2	40000	80000.00	80
138	trackers	3	16000	48000.00	81
139	six months new subscriptions	6	5000	30000.00	81
140	installation	2	3000	6000.00	81
141	sim card	2	1000	2000.00	81
142	tracker subscription renewal	5	15000	75000.00	82
143	Ecommerce sales in september	1	169200	169200.00	83
157	two tracker devices	2	17000	34000.00	87
158	installation	3500	2	7000.00	87
159	tracker sim	2	1200	2400.00	87
160	subscription for 6months	2	12000	24000.00	87
180	tracker installation	1	4000	4000.00	97
181	Tracker sim	1	3500	3500.00	97
182	tracker devices	2	17000	34000.00	98
183	tracker sims	2	3500	7000.00	98
190	merchant app development	1	350000	350000.00	99
185	installation fee	2	4000	8000.00	98
161	server hosting cost (NGN) for six months	6	12000	72000.00	88
162	Inventory Software Development	1	1282000	1282000.00	89
164	Sales in October	1	283100	283100.00	90
165	laptop bags	1	10500	10500.00	91
166	laptop bag	1	18000	18000.00	91
167	Laptop bag	1	19000	19000.00	92
168	laptop - coolbell	1	15500	15500.00	93
169	application support for 2022	12	10000	120000.00	94
170	tracker device	10	17000	170000.00	95
171	annual running subscription	12	25000	300000.00	95
172	sim registration	10	3000	30000.00	95
173	installation cost	10	4500	45000.00	95
176	sim devices	2	3000	6000.00	96
177	installation fee	2	4000	8000.00	96
174	tracker devices	2	20000	40000.00	96
175	annual subscription	12	4000	48000.00	96
150	subscription fee annual charge	12	5000	60000.00	85
147	annual subscription	12	2000	24000.00	84
191	customer app development	1	200000	200000.00	99
192	admin portal development	1	200000	200000.00	99
193	Payment for tracker renewal	5	15000	75000.00	100
194	subscription	2	15000	30000.00	101
178	tracker devies	1	17000	17000.00	97
179	tracker service subscription	12	2000	24000.00	97
196	annual server maintenance	1	30000	30000.00	102
184	tracker annual subscription	12	4000	48000.00	98
195	Server hosting cost	6	14000	84000.00	102
197	laptop bags	32	12500	400000.00	103
198	Capricon API readjustment	1	200000	200000.00	104
199	laptop bag	1	16500	16500.00	105
163	annual server setup, configuration and troubleshooting	1	168000	168000.00	89
200	delivery fee from mainland	1	2500	2500.00	105
201	laptop bag	1	15000	15000.00	106
202	delivery fee	1	2000	2000.00	106
203	server hosting cost for 6 months	6	14000	84000.00	107
204	tracker subscription for one year	12	2000	24000.00	108
205	ecommerce transacition for January	1	211000	211000.00	109
206	February ecommerce sales	1	89000	89000.00	110
207	support fee for 2023	1	120000	120000.00	111
209	designs 	1	250000	250000.00	112
210	deployments and hosting 1 year	1	200000	200000.00	112
271	delivery charges	1	15000	15000.00	150
211	application development for 4 months (android app, api, admin backend)\r\nserver shared hosting for one year;\r\n6 months free support after deployment; 	1	2500000	2500000.00	113
212	Android app development	1	2000000	2000000.00	114
215	project deployment, one year hosting fee & miscellenous	1	1000000	1000000.00	114
272	laptop bags	1	221000	221000.00	151
216	personal tracker device	1	23000	23000.00	115
217	laptop bags 	1	68000	68000.00	116
218	Ecommerce sales activity	1	367000	367000.00	117
219	annual maintance	1	50000	50000.00	118
220	server cost for 6 months	6	15000	90000.00	118
213	Headless API for client Interface 	1	1000000	1000000.00	114
214	backend application for operations management	1	2000000	2000000.00	114
221	tracker and Map monitoring platform	1	25000	25000.00	119
222	google map for monitoring	1	10000	10000.00	119
223	tracker installation	1	6000	6000.00	119
224	laptop bag sales	1	299300	299300.00	120
225	laptop bag	15000	1	15000.00	120
227	installation	2	9000	18000.00	121
229	google map UI ( per annum)	4	10000	40000.00	121
230	data mgt per annum	4	4000	16000.00	121
231	laptop bags 	1	314500	314500.00	122
226	two tracker wires replacement	2	2000	4000.00	121
232	tracker device	1	25000	25000.00	123
233	google map access	1	10000	10000.00	123
234	installation charges	1	9000	9000.00	123
235	laptop bag sales	1	97000	97000.00	124
236	Laptop bags	1	293600	293600.00	125
273	laptop bag sales	1	291000	291000.00	152
208	application development 4 months period	6	850000	5100000.00	112
237	server hosting for 2 months	2	16000	32000.00	126
238	laptop bag sales	1	256000	256000.00	127
239	server hosting from Nov 16th to Jan 15th	2	16000	32000.00	128
240	cloud server hosting dec to may 	6	20000	120000.00	129
241	Maintenance charges for 6 months	1	50000	50000.00	129
242	tracker hardware device	1	20000	20000.00	130
243	tracker installation	1	5000	5000.00	130
244	laptop bags	1	287000	287000.00	131
245	laptop bag 25L capacity 	1	29000	29000.00	132
246	delivery charge	1	3000	3000.00	132
247	laptop bag 	1	12000	12000.00	133
248	transport charges	1	3000	3000.00	133
249	laptop bag sales	1	640000	640000.00	134
250	server hosting from Jan 16th to March 15th	2	16000	32000.00	135
251	support fee for 2023	1	120000	120000.00	136
252	landing page implementation, mobile and web layout	1	500000	500000.00	137
274	laptop back packs - black color	10	20000	200000.00	153
253	digoshoppa product feature request	1	320000	320000.00	138
254	laptop bag sales 	1	189000	189000.00	139
255	laptop bags	1	388500	388500.00	140
257	tracker installation	1	10000	10000.00	141
256	tracker device and monitoring platform	1	25000	25000.00	141
258	laptop bag	1	22000	22000.00	142
259	delivery	1	3000	3000.00	142
260	server hosting for March 16th to May 15th	1	32000	32000.00	143
261	laptop bag sales	1	366000	366000.00	144
262	laptop bags	1	1130000	1130000.00	145
263	landing page	1	50000	50000.00	146
264	shared hosting may 16th to July 15th 	1	32000	32000.00	147
266	maintenance charges	1	50000	50000.00	148
267	laptop bag	1	22000	22000.00	149
268	waybill	1	3500	3500.00	149
265	server hosting for June to Nov	6	28000	168000.00	148
269	laptop bag	9	20000	180000.00	150
270	outstanding charge	1	3000	3000.00	150
275	server hosting renewal july 16th  to sept 15h	2	16000	32000.00	154
276	laptop bag sales	1	209500	209500.00	155
277	laptop bag	9	20000	180000.00	156
279	Bullionsms Integration Fee	1	80000	80000.00	157
278	delivery charges	1	8000	8000.00	156
\.


--
-- Data for Name: payment; Type: TABLE DATA; Schema: public; Owner: sysdba
--

COPY public.payment (id, client_name, payment_desc, date_created, payment_mode, amount_paid, balance, invoice_id, status) FROM stdin;
1	Credit Switch Ltd	Payment for Project Implementation	2020-01-14 16:10:28.039493	2	1200000.00	20000.00	1	2
3	Agulanna Josemaria Michael Jidizu	Part payment for the Training Class	2020-01-20 16:10:28.039493	1	65000.00	0.00	3	1
2	Oladiran Matthew	Part payment for Data Science class	2020-01-24 16:10:28.039493	3	65000.00	0.00	2	1
4	Fatogun Alex	Part Payment for Personal Python Class	2020-01-23 16:10:28.039493	2	80000.00	20000.00	4	2
5	Mary Olunuga	Payment for Installation and and Device Setup	2020-02-25 16:10:28.039493	2	27000.00	0.00	5	1
6	Elegah Joseph	Registration Payment for Datascience	2020-03-09 16:10:28.039493	3	65000.00	0.00	6	1
7	Obinaya Chibike	Registration Fee Payment	2020-03-04 16:10:28.039493	2	40000.00	0.00	7	1
8	Uzodinma Jeff	Cash injection to the business	2020-03-31 18:27:33.342833	2	330000.00	0.00	11	1
9	Ibrahim Bashir	First initial payment made.	2020-04-24 16:27:53.006369	2	50000.00	702500.00	12	2
50	ECOMMERCE	full payment	2021-04-07 09:05:15.363476	2	6500.00	0.00	42	1
10	Ibrahim Bashir	vat on 50k	2020-04-24 16:52:33.949289	2	3570.00	698930.00	12	2
11	Ibrahim Bashir	Second installment payment made	2020-04-30 23:20:29.071038	2	53570.00	645360.00	12	2
12	Ibrahim Bashir	third installment payment	2020-05-27 10:27:56.539859	2	107500.00	537860.00	12	2
13	Habib	full payment for one year	2020-06-29 16:40:53.723394	2	48375.00	0.00	13	1
14	Mobifin Services Ltd	kick off payment for capricon intgrations	2020-07-02 13:55:58.9389	2	262000.00	301300.00	10	2
15	Ibrahim Bashir	third payments	2020-07-02 16:44:25.592996	2	107500.00	430360.00	12	2
16	Bankola Wickliffe	full payments	2020-07-14 10:48:07.474883	2	30100.00	0.00	14	1
17	Ibrahim Bashir	part payment	2020-07-23 11:53:59.682527	2	53750.00	376610.00	12	2
18	LEAPE	first startup payment	2020-08-03 20:07:16.103673	2	1500000.00	3337500.00	15	2
19	ONE PLUG VENTURES	complete payment	2020-08-16 18:32:13.626125	2	70950.00	0.00	16	1
20	Casia Growth Lab	first installment payment	2020-10-01 15:56:02.845951	2	190000.00	190000.00	17	2
21	Jimoh Ernest	full payment for maptrackapp	2020-10-02 15:56:46.426671	2	24188.00	-0.50	18	1
22	Jimoh Ernest	subscription for november	2020-11-05 19:06:51.79561	2	3500.00	0.00	19	1
23	Ibrahim Bashir	part payment	2020-11-18 13:22:16.915486	2	35000.00	341610.00	12	2
24	Ibrahim Bashir	part payment 	2020-11-19 11:07:22.737512	2	35000.00	306610.00	12	2
25	Mobifin Services Ltd	first payment	2020-12-11 14:13:32.514464	2	45687.00	45688.00	20	2
26	Konverse Logistics	full payment for tracker installation	2020-12-15 14:45:43.495385	2	36550.00	0.00	21	1
27	Ibrahim Bashir	part payment remittance	2020-12-15 15:49:53.677434	2	50000.00	256610.00	12	2
28	Mobifin Services Ltd	balance payment	2020-12-30 12:06:08.271614	2	45688.00	45688.00	20	1
29	Mobifin Services Ltd	balance payment	2020-12-30 12:08:49.30205	2	301300.00	0.00	10	1
30	Ibrahim Bashir	part payments	2021-01-01 14:24:45.513143	2	100000.00	156610.00	12	2
31	LEAPE	second installment payment	2021-01-08 15:22:10.710373	2	1500000.00	1837500.00	15	2
32	ONE PLUG VENTURES	full payment for tracker installation	2021-01-18 19:59:01.623885	2	33862.50	0.00	22	1
33	phummiekush	full payment	2021-01-30 21:08:37.017044	2	114000.00	-587.50	23	1
35	Jimoh Ernest	complete payment online	2021-01-29 10:36:02.438317	3	3500.00	262.50	26	1
34	OWOLABI TAIBAT	full payment for tracking service	2021-01-31 11:36:02.438317	2	24187.50	0.00	24	1
36	ONE PLUG VENTURES	paid in full	2021-02-13 09:30:28.01475	2	45000.00	3375.00	27	1
37	Jimoh Ernest	full payment	2021-02-25 12:11:13.578868	2	27950.00	0.00	25	1
38	OWOLABI TAIBAT	full payment - vat absorbed	2021-03-01 21:13:18.478708	2	3500.00	262.50	28	1
39	phummiekush	full payment less vat	2021-03-02 14:49:28.13855	2	12500.00	937.50	29	1
40	HODAYAH'S LOGISTICS	payment for tracker and installation	2021-03-03 19:36:12.538563	2	35000.00	2625.00	30	1
41	ECOMMERCE	complete payment	2021-03-05 16:17:43.315622	2	14000.00	0.00	32	1
42	ECOMMERCE	paid complete	2021-03-05 21:36:43.341425	2	7000.00	0.00	33	1
43	Abisola Roland	full payment	2021-03-07 21:45:14.641091	2	24187.50	0.00	31	1
44	ECOMMERCE	full payment	2021-03-08 10:49:41.733558	2	14000.00	0.00	34	1
45	ECOMMERCE	full payment	2021-03-08 10:58:12.71881	2	24000.00	0.00	35	1
46	ECOMMERCE	payment for fitness wrist watch	2021-03-18 17:13:17.666172	2	7000.00	0.00	37	1
47	ECOMMERCE	full payment	2021-03-28 10:12:01.794479	2	4000.00	0.00	38	1
48	Abisola Roland	full payment for subscription	2021-04-05 08:41:59.353046	2	3500.00	262.50	40	1
49	ECOMMERCE	nil	2021-04-05 14:15:09.11374	2	6000.00	0.00	41	1
51	Bankola Wickliffe	full payment	2021-04-07 11:24:59.552661	2	40850.00	0.00	43	1
52	ECOMMERCE	nil	2021-04-09 12:39:34.468018	2	15000.00	0.00	44	1
53	ECOMMERCE	nil	2021-04-09 17:50:49.558394	2	6500.00	0.00	45	1
54	ECOMMERCE	nil	2021-04-09 17:51:09.729449	2	6500.00	0.00	46	1
55	ECOMMERCE	nil	2021-04-12 00:12:56.607536	2	6500.00	0.00	48	1
56	Ibrahim Bashir	thanks	2021-04-16 12:43:52.226202	2	107000.00	49610.00	12	2
57	ECOMMERCE	nil	2021-04-18 18:33:44.725981	2	26000.00	0.00	49	1
58	ONE PLUG VENTURES	nil	2021-04-20 11:39:31.492258	2	61275.00	0.00	39	1
59	ECOMMERCE	nil	2021-04-20 11:41:32.00215	2	10000.00	0.00	50	1
60	Oxford logistics	nil	2021-04-20 21:41:55.30335	2	99438.00	-0.50	47	1
61	ECOMMERCE	nil	2021-04-22 07:30:40.573342	2	6500.00	0.00	51	1
62	ECOMMERCE	nil	2021-04-22 14:40:50.485034	2	6500.00	0.00	52	1
63	ECOMMERCE	nil	2021-04-23 09:14:17.128316	2	6000.00	0.00	53	1
64	ECOMMERCE	nil	2021-04-27 19:32:44.694777	2	6000.00	0.00	56	1
65	Jimoh Ernest	nil	2021-05-05 10:50:54.15415	2	3500.00	0.00	58	1
66	Abisola Roland	full payment	2021-05-10 19:35:59.816928	2	30000.00	0.00	59	1
67	Mobifin Services Ltd	complete payment	2021-05-15 09:31:28.069649	2	96750.00	0.00	60	1
68	Habib	nil	2021-05-24 10:17:01.558306	2	16000.00	1200.00	55	1
69	ONE PLUG VENTURES	nil	2021-06-14 09:28:58.350298	2	73000.00	637.50	54	2
70	HODAYAH'S LOGISTICS	full payment	2021-06-30 09:27:50.744973	2	37625.00	0.00	62	1
71	ECOMMERCE	nil	2021-07-04 20:24:40.998859	2	9000.00	0.00	63	1
72	ECOMMERCE	nil	2021-07-05 14:33:14.423439	2	9000.00	0.00	64	1
73	ECOMMERCE	nil	2021-07-05 19:57:59.27326	2	9000.00	0.00	65	1
74	Ibrahim Bashir	balance payment	2021-07-06 13:33:42.835076	2	50000.00	-390.00	12	1
75	ECOMMERCE	nil\r\n	2021-07-12 07:52:51.341426	2	9000.00	0.00	66	1
76	ECOMMERCE	nil	2021-07-12 07:53:34.724006	2	8000.00	0.00	67	1
77	ECOMMERCE	nil	2021-07-12 12:38:36.139312	2	9000.00	0.00	69	1
78	ECOMMERCE	nil	2021-07-14 19:32:16.474424	2	16000.00	0.00	70	1
79	ECOMMERCE	nil\r\n	2021-07-17 12:07:47.226161	2	9000.00	0.00	72	1
80	Bankola Wickliffe	nil	2021-07-17 12:09:00.591698	2	7000.00	525.00	73	1
81	ECOMMERCE	nil	2021-07-21 20:55:40.583215	2	18000.00	0.00	71	1
82	ECOMMERCE	nil	2021-07-23 13:52:16.148338	2	9000.00	0.00	74	1
83	ECOMMERCE	nil	2021-07-27 09:34:02.564583	2	8500.00	0.00	75	1
84	Umunah Peace	First payment for the class	2021-07-30 18:25:11.556618	2	40000.00	50000.00	77	2
85	ECOMMERCE	nil	2021-08-01 23:06:49.480567	2	8500.00	0.00	76	1
86	Chukwuka Paul Chukwuebuka	nil	2021-08-09 08:38:30.977577	2	100000.00	100000.00	80	2
87	Uwannah Peace	nil	2021-09-02 10:12:23.124736	2	50000.00	0.00	77	1
88	LEAPE	third installment	2021-09-16 09:00:19.93911	2	800000.00	1037500.00	15	2
89	ONE PLUG VENTURES	nil	2021-09-24 08:54:08.297691	2	92450.00	0.00	81	1
90	ONE PLUG VENTURES	nil	2021-09-16 08:54:08.297691	2	75000.00	5625.00	82	1
91	ECOMMERCE	nil	2021-09-30 09:46:59.970451	2	169200.00	0.00	83	1
92	Adrielle Logistics Services	nil	2021-11-02 13:08:24.306804	2	72455.00	0.00	87	1
93	AJALA ANTHONY JOACHIN	project kick off payment	2021-11-13 09:50:48.253063	2	725000.00	725000.00	89	2
94	ECOMMERCE	nil	2021-10-31 12:35:31.728901	2	283100.00	0.00	90	1
95	Mobifin Services Ltd	nil	2021-11-15 16:26:18.931286	2	71595.00	0.00	88	1
96	ECOMMERCE	nil	2021-12-04 11:21:29.539545	2	28500.00	0.00	91	1
97	ECOMMERCE	nil	2021-12-13 21:51:25.670272	2	19000.00	0.00	92	1
98	ECOMMERCE	nil	2022-01-14 17:41:18.864565	2	15500.00	0.00	93	1
99	Mr. Ayodeji Bidemi Adebayo	nil	2022-02-05 21:39:16.85782	2	96000.00	0.00	96	1
100	JadeandMary	nil	2022-03-04 14:57:22.574515	2	120000.00	0.00	94	1
101	ONE PLUG VENTURES	part payment to balance by month end	2022-04-13 12:36:36.681251	2	50000.00	30625.00	100	2
102	Mobifin Services Ltd	payment complete	2022-05-10 17:03:55.827576	2	114000.00	0.00	102	1
103	ONE PLUG VENTURES	nil	2022-05-19 15:47:26.264235	2	25000.00	5625.00	100	1
104	ONE PLUG VENTURES	part payment	2022-05-19 15:48:15.628061	2	15000.00	15000.00	101	2
105	Hoowfar App	first deposite	2022-06-23 10:07:02.454583	2	200000.00	550000.00	99	2
106	Mobifin Services Ltd	first payment	2022-06-23 10:08:50.03849	2	107500.00	107500.00	104	2
107	Mobifin Services Ltd	bal payment	2022-07-07 17:54:57.095325	2	107500.00	0.00	104	1
108	AJALA ANTHONY JOACHIN	full payment	2022-08-04 14:24:26.267661	2	725000.00	0.00	89	1
109	Critters Veterinary Centre	nil	2022-10-18 10:54:25.688341	2	19000.00	0.00	105	1
110	Kumar medewar	nil	2022-11-22 08:28:38.062228	2	17000.00	0.00	106	1
111	Mobifin Services Ltd	nil	2022-11-30 14:16:20.180546	2	84000.00	0.00	107	1
112	ECOMMERCE	nil	2023-01-31 18:19:55.258512	2	211000.00	0.00	109	1
113	ECOMMERCE	nil	2023-02-27 08:42:19.352201	2	89000.00	0.00	110	1
114	Maptrackapp	part payment	2023-03-31 13:18:28.495245	2	14000.00	9000.00	115	2
115	ECOMMERCE	nil	2023-03-31 21:33:03.202309	2	68000.00	0.00	116	1
116	ECOMMERCE	nil	2023-04-30 08:48:53.011751	2	367000.00	0.00	117	1
117	Mobifin Services Ltd	nil	2023-05-15 17:11:26.508351	2	140000.00	0.00	118	1
118	Zillionaire Media Global Services Limited	first deposit payment	2023-05-20 19:20:15.985831	2	1500000.00	1000000.00	113	2
119	Zillionaire Media Global Services Limited	first deposit	2023-05-20 19:45:15.703686	2	3600000.00	2400000.00	114	2
120	Ubosi Stanley R	payment complete	2023-05-23 14:02:48.388516	2	41000.00	0.00	119	1
121	ECOMMERCE	nil	2023-05-30 19:36:10.758586	2	299300.00	0.00	120	1
122	ECOMMERCE	nil	2023-05-30 23:02:05.422555	2	15000.00	0.00	120	1
123	ECOMMERCE	nil	2023-06-30 15:25:18.6468	2	314500.00	0.00	122	1
124	ONE PLUG VENTURES	nil	2023-07-11 11:44:17.569943	2	78000.00	0.00	121	1
125	Ubosi Stanley R	nil	2023-07-12 12:26:33.377989	2	44000.00	0.00	123	1
126	ECOMMERCE	nil	2023-07-31 21:02:17.662992	2	97000.00	0.00	124	1
127	ECOMMERCE	nil	2023-08-31 09:08:49.467891	2	293600.00	0.00	125	1
128	JadeandMary	nil	2023-09-11 08:26:25.269583	2	120000.00	0.00	111	1
129	JadeandMary	nil	2023-09-26 20:31:14.810593	2	32000.00	0.00	126	1
130	ECOMMERCE	nil	2023-09-30 02:57:55.28924	2	256000.00	0.00	127	1
131	Mobifin Services Ltd	nil	2023-11-16 16:53:05.097927	2	170000.00	0.00	129	1
132	JadeandMary	nil	2023-11-21 14:23:10.912751	2	32000.00	0.00	128	1
133	Uhegbu Emeka	nil	2023-11-22 09:47:27.461534	2	25000.00	0.00	130	1
134	ECOMMERCE	nil	2023-11-30 18:20:02.375454	2	287000.00	0.00	131	1
135	Zillionaire Media Global Services Limited	second installment	2023-12-08 20:19:40.063796	2	500000.00	500000.00	113	2
136	Michael Emerue	nil	2023-12-12 16:17:42.049609	2	32000.00	0.00	132	1
137	Bolatito Ayodele	nil	2023-12-14 19:08:14.312056	2	15000.00	0.00	133	1
138	ECOMMERCE	nil	2023-12-31 10:21:20.527225	1	640000.00	0.00	134	1
139	Zillionaire Media Global Services Limited	nil	2024-01-09 13:33:09.553582	2	500000.00	0.00	113	1
140	JadeandMary	nil	2024-01-29 13:19:18.006515	2	32000.00	0.00	135	1
141	ECOMMERCE	nil	2024-01-30 14:45:34.671353	2	189000.00	0.00	139	1
142	ECOMMERCE	nil	2024-02-29 12:53:23.701643	2	388500.00	0.00	140	1
143	Dike John Uchechukwu	nil	2024-03-07 08:47:09.174118	2	35000.00	0.00	141	1
144	JadeandMary	nil	2024-03-20 08:03:33.688074	2	120000.00	0.00	136	1
145	ECOMMERCE	nil	2024-04-01 08:40:01.368445	2	366000.00	0.00	144	1
146	JadeandMary	nil	2024-04-03 09:51:35.832521	2	32000.00	0.00	143	1
147	ECOMMERCE	nil	2024-04-26 08:23:34.274157	2	1077000.00	0.00	145	1
148	ECOMMERCE	nil	2024-04-30 19:32:48.848844	2	53000.00	0.00	145	1
149	Nigeria Network of NGOs	nil	2024-05-07 15:17:48.293884	2	25500.00	0.00	149	1
150	Mobifin Services Ltd	nil	2024-05-16 19:00:59.282791	2	218000.00	0.00	148	1
151	JadeandMary	nil	2024-05-23 10:36:45.515031	2	40000.00	0.00	146	1
152	JadeandMary	nil	2024-05-23 10:37:21.531703	2	32000.00	0.00	147	1
153	ECOMMERCE	nil	2024-05-30 09:02:11.895829	2	177500.00	0.00	151	1
154	ECOMMERCE	nil	2024-05-31 20:48:23.539842	2	43500.00	0.00	151	1
155	ECOMMERCE	nil	2024-06-30 04:49:28.781959	2	291000.00	0.00	152	1
156	Ralds and Agate Limited	nil	2024-07-18 08:18:53.506277	2	200000.00	0.00	153	1
157	ECOMMERCE	nil	2024-07-30 20:40:53.993539	2	209500.00	0.00	155	1
158	JadeandMary	nil	2024-07-31 17:56:05.685522	2	32000.00	0.00	154	1
159	Nigeria Network of NGOs	nil	2024-08-12 14:05:10.168962	2	195000.00	0.00	156	1
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: sysdba
--

COPY public.users (id, username, password) FROM stdin;
1	jeffrey@ecardex.com	pbkdf2:sha256:150000$LFLfgkLg$dee63cb999968e96aa0de03d21373484ebc671b420d54160aa893a72bb1a4732
\.


--
-- Name: client_invoice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sysdba
--

SELECT pg_catalog.setval('public.client_invoice_id_seq', 55, true);


--
-- Name: email_queue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sysdba
--

SELECT pg_catalog.setval('public.email_queue_id_seq', 1, false);


--
-- Name: email_receipt_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sysdba
--

SELECT pg_catalog.setval('public.email_receipt_id_seq', 26, true);


--
-- Name: expense_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sysdba
--

SELECT pg_catalog.setval('public.expense_id_seq', 653, true);


--
-- Name: invoice_inv_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sysdba
--

SELECT pg_catalog.setval('public.invoice_inv_id_seq', 157, true);


--
-- Name: item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sysdba
--

SELECT pg_catalog.setval('public.item_id_seq', 279, true);


--
-- Name: payment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sysdba
--

SELECT pg_catalog.setval('public.payment_id_seq', 159, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sysdba
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- Name: client client_pkey; Type: CONSTRAINT; Schema: public; Owner: sysdba
--

ALTER TABLE ONLY public.client
    ADD CONSTRAINT client_pkey PRIMARY KEY (id);


--
-- Name: email_queue email_queue_pkey; Type: CONSTRAINT; Schema: public; Owner: sysdba
--

ALTER TABLE ONLY public.email_queue
    ADD CONSTRAINT email_queue_pkey PRIMARY KEY (id);


--
-- Name: email_receipt_count email_receipt_count_pkey; Type: CONSTRAINT; Schema: public; Owner: sysdba
--

ALTER TABLE ONLY public.email_receipt_count
    ADD CONSTRAINT email_receipt_count_pkey PRIMARY KEY (id);


--
-- Name: expense expense_pkey; Type: CONSTRAINT; Schema: public; Owner: sysdba
--

ALTER TABLE ONLY public.expense
    ADD CONSTRAINT expense_pkey PRIMARY KEY (id);


--
-- Name: invoice invoice_pkey; Type: CONSTRAINT; Schema: public; Owner: sysdba
--

ALTER TABLE ONLY public.invoice
    ADD CONSTRAINT invoice_pkey PRIMARY KEY (id);


--
-- Name: item item_pkey; Type: CONSTRAINT; Schema: public; Owner: sysdba
--

ALTER TABLE ONLY public.item
    ADD CONSTRAINT item_pkey PRIMARY KEY (id);


--
-- Name: payment payment_pkey; Type: CONSTRAINT; Schema: public; Owner: sysdba
--

ALTER TABLE ONLY public.payment
    ADD CONSTRAINT payment_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: sysdba
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: invoice invoice_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sysdba
--

ALTER TABLE ONLY public.invoice
    ADD CONSTRAINT invoice_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.client(id);


--
-- Name: item item_invoice_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sysdba
--

ALTER TABLE ONLY public.item
    ADD CONSTRAINT item_invoice_id_fkey FOREIGN KEY (invoice_id) REFERENCES public.invoice(id);


--
-- Name: payment payment_invoice_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sysdba
--

ALTER TABLE ONLY public.payment
    ADD CONSTRAINT payment_invoice_id_fkey FOREIGN KEY (invoice_id) REFERENCES public.invoice(id);


--
-- PostgreSQL database dump complete
--

