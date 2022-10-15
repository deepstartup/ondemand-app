from flask import Flask
from flask import request
import json
from config import config
from postgre_conn_all import connect
import random, string
import psycopg2
from flask_cors import CORS, cross_origin


app = Flask(__name__)

cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_ALLOW_ALL_ORIGINS'] = True
app.config['CORS_ORIGIN_WHITELIST'] = ('http://localhost:3000', 'http://localhost:3002','localhost:3002','http://127.0.0.1:3002')
@cross_origin()


@app.route("/subscriber/create",  methods = ['POST'])
def createSubscriber():
    json_text=request.get_json()
    first_name=json_text['subFirstName']
    last_name=json_text['subLastName']
    dob=json_text['subDOB']
    mob_num=json_text['subMobileNumber']
    gender=json_text['subGender']
    occupation=json_text['subOccupation']
    params_all=config()
    main_conn=connect(params_all)
    postgres_insert_query = """ INSERT INTO subscriber_master ("Subs_first_name", subs_last_name, "SUBS_DOB",subs_mobile_no,"Sub_Gender","Sub_Occupation",sub_activation_flg) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    record_to_insert = (first_name,last_name,dob,mob_num,gender,occupation,'Y')
    main_conn.do_insert(postgres_insert_query,record_to_insert)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/campaign/create",  methods = ['POST'])
def createCampaign():
    json_text=request.get_json()
    camp_name=json_text['campName']
    camp_start_date=json_text['campStartDate']
    camp_end_date=json_text['campEndDate']
    max_subs_allowed=json_text['campMaxSubscriberAllowed']
    total_umb_camp_amt=json_text['campTotalUmbrellaAmount']
    camp_sub_fees=json_text['campSubscribtionFees']
    camp_allow_no_inst=json_text['campNumberOfAllowedInstallment']
    params_all=config()
    main_conn=connect(params_all)
    postgres_insert_query = """INSERT INTO public.camp_master(camp_name, camp_start_date, camp_end_date, max_subs_allowed, total_umb_camp_amt, camp_sub_fees, camp_allow_no_inst, camp_activation_flg) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    record_to_insert = (camp_name, camp_start_date, camp_end_date, max_subs_allowed, total_umb_camp_amt, camp_sub_fees, camp_allow_no_inst,True)
    main_conn.do_insert(postgres_insert_query,record_to_insert)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/services/create",  methods = ['POST'])
def createSCConnect():
    json_text=request.get_json()
    serviceId=json_text['serviceId']
    serviceName=json_text['serviceName']
    serviceDescription=json_text['serviceDescription']
    serviceStartDate=json_text['serviceStartDate']
    serviceEndDate=json_text['serviceEndDate']
    serviceActiveFlag=json_text['serviceActiveFlag']
    #subscription_activation_date=json_text['subscriptionActivationDate']
    params_all=config()
    main_conn=connect(params_all)
    postgres_insert_query = """INSERT INTO kvx_db_prod.kvx_services
        (service_id, service_name, service_description, service_start_date, service_end_date, service_active_flag) VALUES (%s,%s,%s,%s,%s,%s)"""
    record_to_insert = (serviceId, serviceName, serviceDescription, serviceStartDate, serviceEndDate, serviceActiveFlag)
    main_conn.do_insert(postgres_insert_query,record_to_insert)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/subcamppayment/create",  methods = ['POST'])
def createPayment():
    json_text=request.get_json()
    txn_date=json_text['txnDate']
    txn_timestamp=json_text['txnTimeStamp']
    txn_amount=json_text['txnAmount']
    txn_status=json_text['txnStatus']
    subs_id=json_text['subID']
    camp_id=json_text['campID']
    external_upi_number=json_text['extUPINumber']
    order_reference_number=json_text['orderRefNumber']
    params_all=config()
    main_conn=connect(params_all)
    postgres_insert_query = """INSERT INTO public.sub_camp_transaction(txn_date,txn_timestamp,txn_amount,txn_status,sub_id,camp_id,external_upi_number,order_ref_no) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    record_to_insert = (txn_date,txn_timestamp,txn_amount,txn_status,subs_id,camp_id,external_upi_number,order_reference_number)
    main_conn.do_insert(postgres_insert_query,record_to_insert)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/subscriberOrder/create",  methods = ['POST'])
def createOrder():
    json_text=request.get_json()
    order_reference_number=''.join(random.choice(string.ascii_uppercase+ string.digits) for _ in range(10))
    subs_id=json_text['subID']
    camp_id=json_text['campID']
    order_date=json_text['orderDate']
    order_amount=json_text['orderAmt']
    ORDER_STATUS=json_text['orderStatus']
    ORDER_MESSAGE=json_text['orderMessage']
    params_all=config()
    main_conn=connect(params_all)
    postgres_insert_query = """INSERT INTO public.subscriber_order_details(order_reference_number,sub_id,camp_id,order_date,order_amount,ORDER_STATUS,ORDER_MESSAGE) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    record_to_insert = (order_reference_number,subs_id,camp_id,order_date,order_amount,ORDER_STATUS,ORDER_MESSAGE)
    main_conn.do_insert(postgres_insert_query,record_to_insert)
    return json.dumps({'success':True,'orderRefNumber':order_reference_number}), 200, {'ContentType':'application/json'}

#####Update service####Diff API#####
@app.route("/subscriberOrder/modify",  methods = ['POST'])
def updateOrder():
    json_text=request.get_json()
    order_reference_number=json_text['orderRefNumber']
    subs_id=json_text['subID']
    camp_id=json_text['campID']
    order_latest_timestamp=json_text['orderTimeStamp']
    ORDER_STATUS=json_text['orderStatus']
    ORDER_MESSAGE=json_text['orderMessage']
    params_all=config()
    main_conn=connect(params_all)
    postgres_update_query = """update public.subscriber_order_details set ORDER_STATUS=%s,order_latest_timestamp=%s,ORDER_MESSAGE=%s where order_reference_number=%s and sub_id=%s and camp_id=%s"""
    record_to_update = (ORDER_STATUS,order_latest_timestamp,ORDER_MESSAGE,order_reference_number,subs_id,camp_id)
    main_conn.do_insert(postgres_update_query,record_to_update)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
#####End of update service########




@app.route("/service/All",  methods = ['GET'])
def SetAllService():
    # json_text=request.get_json()
    params_all=config()
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params_all)
    cur = conn.cursor()
    print('PostgreSQL database version:')
    cur.execute('select * from kvx_db_prod.kvx_services;')
    servicesall = cur.fetchall()
    print('show>>',servicesall)
    cur.close()
    data:list=[]
    for _servicesall in servicesall:
        service_name:dict={'service_id':_servicesall[0],'service_name':_servicesall[1]}
        data.append(service_name)
    print(data)
    return json.dumps(data)


@app.route("/service/service_provider",  methods = ['GET'])
def getServiceProvider():
    # json_text=request.get_json()
    params_all=config()
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params_all)
    cur = conn.cursor()
    print('PostgreSQL database version:')
    cur.execute('select ksp.service_provider_id, ks.sp_enterprice_name  from kvx_db_prod.kvx_service_provider as ksp, kvx_db_prod.kvx_sp_enterprise as ks where ksp.service_provider_id =ks.sp_service_provider_id;')
    servicesall = cur.fetchall()
    print('show>>',servicesall)
    cur.close()
    data:list=[]
    for _servicesall in servicesall:
        service_name:dict={'service_id':_servicesall[0],'service_name':_servicesall[1]}
        data.append(service_name)
    print(data)
    return json.dumps(data)
#added the function for calling the customer booking details view with cust id : example : http://localhost:5001/customer/BookAllView?id=1
@app.route("/customer/BookAllView",  methods = ['GET'])
def CountAllBookingGet():
    params_all=config()
    custId = int(request.args.get('id'))
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params_all)
    cur = conn.cursor()
    print('PostgreSQL database version:')
    query=f'select * from kvx_db_prod.kvx_vw_cust_bk_det where cust_id={custId}'
    cur.execute(query)
    servicesall = cur.fetchall()
    print('show>>',servicesall)
    cur.close()
    data:list=[]
    for _servicesall in servicesall:
        service_name:dict={'service_name':_servicesall[0],'service_description':_servicesall[1],'service_active_flag':_servicesall[2],'service_provider_type':_servicesall[3] ,'service_provider_activation_flag':_servicesall[4],'sp_enterprice_name':_servicesall[5],'sp_enterprice_owner':_servicesall[6],'enterprice_primary_mobile_no':_servicesall[7],'sp_location_type':_servicesall[8],'sp_location_lat':_servicesall[9],'sp_location_long':_servicesall[10],'sp_location_street_add1':_servicesall[11],'sp_location_street_add2':_servicesall[12],'sp_location_city':_servicesall[13],'sp_location_country':_servicesall[14],'sp_location_zip_code':_servicesall[15],'sp_first_name':_servicesall[16],'sp_last_name':_servicesall[17],'sp_gender':_servicesall[18],'individual_primary_mobile_no':_servicesall[19],'order_datetime':_servicesall[20],'order_status':_servicesall[21],'order_type':_servicesall[22],'order_qty':_servicesall[23] ,'payment_type':_servicesall[24],'payment_date_time':_servicesall[25],'payment_amount':_servicesall[26],'rating':_servicesall[27] ,'review_timestamp':_servicesall[28],'review_comments':_servicesall[29],'cust_id':_servicesall[30],'cust_first_name':_servicesall[31],'cust_last_name':_servicesall[32],'cust_primary_mobile_no':_servicesall[33],'cust_location_lat':_servicesall[34],'cust_location_long':_servicesall[35],'cust_location_zip_code':_servicesall[36],'cust_activation_flag':_servicesall[37],'favourite_flag':_servicesall[38],'order_id':_servicesall[39],'reviewer_type':_servicesall[40]}
        data.append(service_name)
    print('data==',data)
    return json.dumps(data,indent=4, sort_keys=True, default=str)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
