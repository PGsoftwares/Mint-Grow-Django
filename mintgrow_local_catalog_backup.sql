--
-- PostgreSQL database dump
--

\restrict gogaSF7RwIMJcvpBRitD6JTNd4DDQHEnpbSczwuXx4CLOyFXnLp1hy1MRyiFidf

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: categories_productcategory; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.categories_productcategory VALUES (2, 'Vegetables', 'Fresh, farm-picked vegetables delivered with quality and freshness you can trust. Choose from a wide range of leafy greens, root vegetables, gourds, and seasonal produce for your everyday cooking needs.', 'vegetables', 'categories/vegetables.jpeg', 'active', '2026-07-20 16:41:48.34616+05:30', '2026-07-31 15:47:39.512303+05:30', NULL);
INSERT INTO public.categories_productcategory VALUES (8, 'Leaves', 'Fresh, aromatic leafy herbs and greens including coriander, curry leaves, mint, spinach, and other farm-fresh varieties for everyday cooking.', 'leaves', 'categories/leaves.jpeg', 'active', '2026-07-31 15:49:21.750826+05:30', '2026-07-31 15:49:21.75084+05:30', NULL);


--
-- Data for Name: home_heroslider; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.home_heroslider VALUES (2, 'Grown with care, delivered with trust', 'From our farmers', 'to your table', 'Fresh, responsibly sourced produce built on strong farmer partnerships and a commitment to quality.', 'View Our Products', '#', 'Discover Our Story', '#', 'hero_sliders/slide2.jpg', '', 0, 'active', '2026-08-18 17:20:21.283116+05:30', '2026-08-18 17:20:21.283128+05:30');
INSERT INTO public.home_heroslider VALUES (3, 'Quality you can trace', 'Better farming for', 'a better future', 'We bring together responsible farming, technology and efficient supply chains to create better food systems.', 'View Our Products', '#', 'Discover Our Story', '#', 'hero_sliders/slide3.jpg', '', 0, 'active', '2026-08-18 17:20:57.498679+05:30', '2026-08-18 17:20:57.498691+05:30');
INSERT INTO public.home_heroslider VALUES (1, 'Farmer-led integrated food company', 'Fresh produce from', 'farm to future', 'We connect farmers, technology and markets to deliver safe, traceable and high-quality agricultural products.', 'View Our Products', '#', 'Discover Our Story', '#', 'hero_sliders/slide1.jpg', '', 0, 'active', '2026-08-18 17:19:31.989535+05:30', '2026-08-18 17:26:45.898496+05:30');


--
-- Data for Name: products_product; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.products_product VALUES (15, 'Tomato Hyb', 'Tomato Hyb', 'Tomato Hyb', 'products/tomato-hybrid-img.jpeg', 'tomato-hyb', false, 'MG003', 'active', '2026-08-10 17:45:13.699469+05:30', '2026-08-14 14:49:20.793657+05:30', 2);
INSERT INTO public.products_product VALUES (14, 'Brinjal Vari', 'Mint Grow Farm Brinjal Vari is cultivated with care and harvested at the right stage to maintain freshness, tenderness, and natural flavor. Each brinjal is carefully selected to provide consistent quality and a smooth texture suitable for everyday cooking.

Ideal for curries, gravies, stir-fries, roasting, and traditional Indian dishes, Brinjal Vari is a versatile vegetable for home and commercial kitchens. Our focus on responsible cultivation and careful handling helps deliver fresh, quality produce from the farm to your table.', 'Fresh Brinjal Vari, carefully grown and harvested for its tender texture, rich flavor, and consistent farm-fresh quality.', 'products/brinjal-vari-img.jpeg', 'brinjal-vari', true, 'MG002', 'active', '2026-08-01 11:40:23.449491+05:30', '2026-08-14 14:49:44.593488+05:30', 2);
INSERT INTO public.products_product VALUES (13, 'Beans', 'Mint Grow Farm Beans are carefully cultivated and harvested to ensure freshness, tenderness, and excellent quality. Selected for their vibrant appearance and crisp texture, our beans are suitable for a wide variety of everyday dishes.

From curries and stir-fries to salads and traditional recipes, these fresh beans provide a versatile addition to your kitchen. We focus on responsible farming, careful handling, and timely harvesting to help maintain their natural taste and freshness from the farm to your table.', 'Fresh, tender beans grown with care and harvested at the right stage to deliver natural flavour, crisp texture, and consistent quality.', 'products/beans-img.jpeg', 'beans', false, 'MG001', 'active', '2026-08-01 11:06:14.679157+05:30', '2026-08-14 17:18:34.295735+05:30', 2);


--
-- Data for Name: products_productpricevariation; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.products_productpricevariation VALUES (4, 'A GRADE', 45.00, 0, '2026-08-01 11:40:23.455999+05:30', '2026-08-14 14:49:44.595348+05:30', 14, 400.00, 'kg');
INSERT INTO public.products_productpricevariation VALUES (5, 'SMALL SIZE', 50.00, 0, '2026-08-01 11:40:23.457274+05:30', '2026-08-14 15:18:19.043201+05:30', 14, 195.00, 'kg');
INSERT INTO public.products_productpricevariation VALUES (1, 'A-GRADE', 50.00, 0, '2026-08-01 11:06:14.695959+05:30', '2026-08-14 17:18:34.30198+05:30', 13, 0.00, 'pcs');
INSERT INTO public.products_productpricevariation VALUES (2, 'B GRADE', 40.00, 0, '2026-08-01 11:06:14.704787+05:30', '2026-08-28 11:24:06.877514+05:30', 13, 209.00, 'kg');
INSERT INTO public.products_productpricevariation VALUES (7, 'PER KG 16-30 Nos', 15.00, 0, '2026-08-10 17:45:13.744049+05:30', '2026-08-29 09:35:50.970556+05:30', 15, 599.00, 'kg');
INSERT INTO public.products_productpricevariation VALUES (3, 'FARM PRICE', 20.00, 0, '2026-08-01 11:40:23.45418+05:30', '2026-08-29 09:42:27.638267+05:30', 14, 398.00, 'kg');
INSERT INTO public.products_productpricevariation VALUES (6, 'PER KG 12-16 Nos', 25.00, 0, '2026-08-10 17:45:13.724625+05:30', '2026-08-29 09:47:54.303405+05:30', 15, 496.00, 'kg');


--
-- Name: categories_productcategory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_productcategory_id_seq', 8, true);


--
-- Name: home_heroslider_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.home_heroslider_id_seq', 3, true);


--
-- Name: products_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_product_id_seq', 15, true);


--
-- Name: products_productpricevariation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_productpricevariation_id_seq', 7, true);


--
-- PostgreSQL database dump complete
--

\unrestrict gogaSF7RwIMJcvpBRitD6JTNd4DDQHEnpbSczwuXx4CLOyFXnLp1hy1MRyiFidf

