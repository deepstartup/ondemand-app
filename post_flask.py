from flask import Flask
from flask import request
import json
from config import config
from postgre_conn_all import connect
import random, string
app = Flask(__name__)

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

@app.route("/subcampconnect/create",  methods = ['POST'])
def createSCConnect():
    json_text=request.get_json()
    subs_id=json_text['subID']
    camp_id=json_text['campID']
    subscription_activation_date=json_text['subscriptionActivationDate']
    params_all=config()
    main_conn=connect(params_all)
    postgres_insert_query = """INSERT INTO public.subs_camp_connect(subs_id,camp_id,subscription_activation_date,activation_flag) VALUES (%s,%s,%s,%s)"""
    record_to_insert = (subs_id,camp_id,subscription_activation_date,'Y')
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

if __name__ == "__main__":
    app.run()