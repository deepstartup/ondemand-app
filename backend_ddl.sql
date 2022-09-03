-- public.camp_event_connect definition

-- Drop table

-- DROP TABLE public.camp_event_connect;

CREATE TABLE public.camp_event_connect (
	campaign_id int4 NOT NULL,
	event_id int4 NOT NULL,
	activation_flag varchar NULL,
	created_by varchar NULL,
	created_timestamp timestamptz NULL,
	updated_by varchar NULL,
	updated_timestamp timestamptz NULL
);

-- public.camp_master definition

-- Drop table

-- DROP TABLE public.camp_master;

CREATE TABLE public.camp_master (
	id int4 NOT NULL,
	camp_name varchar NULL,
	camp_start_date date NULL,
	camp_end_date date NULL,
	max_subs_allowed int8 NULL,
	total_umb_camp_amt float8 NULL,
	camp_sub_fees float8 NULL,
	camp_allow_no_inst int8 NULL,
	camp_activation_flg bool NULL,
	created_by varchar NULL,
	created_timestamp timestamptz NULL,
	updated_by varchar NULL,
	updated_timestamp timestamptz NULL
);

-- public.event_master definition

-- Drop table

-- DROP TABLE public.event_master;

CREATE TABLE public.event_master (
	event_id int4 NOT NULL,
	event_name varchar NULL,
	event_date date NULL,
	activaiton_flag varchar NULL,
	created_by varchar NULL,
	created_timestamp timestamptz NULL,
	updated_by varchar NULL,
	updated_timestamp timestamptz NULL
);

-- public.subs_camp_connect definition

-- Drop table

-- DROP TABLE public.subs_camp_connect;

CREATE TABLE public.subs_camp_connect (
	camp_id int4 NOT NULL,
	subs_id int4 NOT NULL,
	subscription_activation_date date NULL,
	activation_flag varchar NULL,
	created_by varchar NULL,
	created_timestamp timestamptz NULL,
	updated_by varchar NULL,
	updated_timestamp timestamptz NULL
);

-- public.subs_camp_disconnect definition

-- Drop table

-- DROP TABLE public.subs_camp_disconnect;

CREATE TABLE public.subs_camp_disconnect (
	camp_id int4 NOT NULL,
	subs_id int4 NOT NULL,
	unsub_activation_date date NULL,
	unsub_reason varchar NULL,
	unsub_date date NULL,
	created_by varchar NULL,
	created_timestamp timestamptz NULL,
	updated_by varchar NULL,
	updated_timestamp timestamptz NULL
);

-- public.subscriber_master definition

-- Drop table

-- DROP TABLE public.subscriber_master;

CREATE TABLE public.subscriber_master (
	id int4 NOT NULL,
	subs_first_name varchar NULL,--not null(M)
	subs_last_name varchar NULL,
	SUBS_DOB date NULL,-- not null (M) (Datepicker --legal age as per T&C)
	subs_mobile_no varchar NULL,-- not null (M)[+91-(---)]
	subs_id_proof_type varchar NULL, -- dropdown (addhar/pan/voter/passport)
	subs_id_NUMBER varchar NULL,  -- number 
	SubS_Address_line1 varchar NULL, 
	SubS_Address_line2 varchar NULL,
	SubS_City varchar NULL,
	SubS_State varchar NULL,
	SubS_zip_code varchar NULL, 
	SubS_email_id varchar NULL,--validation
	Sub_Gender varchar NULL, --male/female/others 
	Sub_Occupation varchar NULL, -- dropdown (govt/private/self)
	sub_activation_flg varchar NULL,
	created_by varchar NULL,
	created_timestamp timestamptz NULL,
	updated_by varchar NULL,
	updated_timestamp timestamptz NULL,
	subs_creation_date date NULL
);

-- public.subscriber_paymnet_master definition

-- Drop table

-- DROP TABLE public.subscriber_paymnet_master;

CREATE TABLE public.subscriber_paymnet_master (
	sub_id int4 NOT NULL,
	subs_pay_method varchar NULL,
	subs_card_info varchar NULL,
	subs_payment_activ_flg varchar NULL,
	created_by varchar NULL,
	created_timestamp timestamptz NULL,
	updated_by varchar NULL,
	updated_timestamp timestamptz NULL
);

-- public.subscriber_paymnet_master definition

-- Drop table

-- DROP TABLE public.subscriber_paymnet_master;

create table public.sub_camp_transaction (
txn_id int4 NOT NULL,
txn_date date NULL,
txn_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
txn_amount float8,
txn_status char,
sub_id int4 NOT NULL,
camp_id int4 NOT NULL,
order_ref_no varchar NOT NULL,
version_number int4,
Installment_Number int4,
external_upi_number varchar,
external_txn_datetime TIMESTAMP
);


CREATE TABLE public.subscriber_order_details (
	order_id int4 NOT null,
	order_reference_number varchar NOT NULL,
	order_date date NULL,
	ORDER_LATEST_TIMESTAMP TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	sub_id int4 NOT NULL,
    camp_id int4 NOT NULL,
	order_amount FLOAT NOT NULL,
	ORDER_STATUS CHAR NOT NULL,
	ORDER_MESSAGE VARCHAR NULL,
	created_by varchar NULL,
	created_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	updated_by varchar NULL,
	updated_timestamp TIMESTAMP NULL
);


ALTER TABLE sub_camp_transaction ADD PRIMARY KEY (txn_id);
ALTER TABLE subscriber_paymnet_master ADD PRIMARY KEY (sub_id);
ALTER TABLE subscriber_master ADD PRIMARY KEY (id);
alter table subs_camp_disconnect add primary key(camp_id,subs_id);
alter table subs_camp_connect add primary key(camp_id,subs_id);
alter table event_master add primary key (event_id);
alter table camp_master add primary key (id);
alter table camp_event_connect add primary key (campaign_id,event_id);
alter table subscriber_order_details add primary key (order_id,order_reference_number);

ALTER TABLE sub_camp_transaction
ADD CONSTRAINT sub_txn_fk
FOREIGN KEY (sub_id)
REFERENCES subscriber_master(id)
ON DELETE CASCADE;

ALTER TABLE sub_camp_transaction
ADD CONSTRAINT event_txn_fk
FOREIGN KEY (camp_id)
REFERENCES camp_master(id)
ON DELETE CASCADE;

ALTER TABLE subscriber_paymnet_master
ADD CONSTRAINT sub_pay_fk
FOREIGN KEY (sub_id)
REFERENCES subscriber_master(id)
ON DELETE CASCADE;

ALTER TABLE subs_camp_connect
ADD CONSTRAINT sub_conn_fk
FOREIGN KEY (subs_id)
REFERENCES subscriber_master(id)
ON DELETE CASCADE;

ALTER TABLE subs_camp_connect
ADD CONSTRAINT camp_conn_fk
FOREIGN KEY (camp_id)
REFERENCES camp_master(id)
ON DELETE CASCADE;

alter table camp_event_connect
add constraint event_connt_fk
FOREIGN KEY (event_id)
REFERENCES event_master(event_id)
ON DELETE CASCADE;

alter table camp_event_connect
add constraint camp_connt_fk
FOREIGN KEY (campaign_id)
REFERENCES camp_master(id)
ON DELETE CASCADE;

alter table subscriber_order_details
add constraint order_camp_fk
FOREIGN KEY (camp_id)
REFERENCES camp_master(id)
ON DELETE CASCADE;

alter table subscriber_order_details
add constraint order_sub_fk
FOREIGN KEY (sub_id)
REFERENCES subscriber_master(id)
ON DELETE CASCADE;

alter table sub_camp_transaction
add constraint payment_fk
FOREIGN KEY (order_ref_no)
REFERENCES subscriber_order_details(order_id)
ON DELETE CASCADE;


---------------------------
CREATE SEQUENCE seq_subs_master_id OWNED BY public.subscriber_master.id;
ALTER TABLE public.subscriber_master ALTER COLUMN id SET DEFAULT nextval('seq_subs_master_id');
---------------------------
CREATE SEQUENCE seq_order_id OWNED BY public.subscriber_order_details.order_id;
ALTER TABLE public.subscriber_order_details ALTER COLUMN order_id SET DEFAULT nextval('seq_order_id');
---------------------------
CREATE SEQUENCE seq_payment_id OWNED BY public.sub_camp_transaction.txn_id;
ALTER TABLE public.sub_camp_transaction ALTER COLUMN txn_id SET DEFAULT nextval('seq_payment_id');
---------------------------
