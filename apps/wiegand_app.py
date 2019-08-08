import appdaemon.plugins.hass.hassapi as hass
import datetime
import appdaemon.plugins.mqtt.mqttapi as mqtt
import json
import sqlite3

class WiegandApp(hass.Hass):
    def initialize(self):
        #gather instance parameters
        self.set_namespace("hass")
        self.mqtt = self.get_app("ha_mqtt")
  
        # load parmeters
        self.sqlite_database = self.args.get('sqlite_database', 'db.sqlite3')
        self.counter_limit = self.args.get('counter_limit', 3)
        self.pin_size = self.get('pin_size',9999)
        self.pin_message = self.get('pin_message','your new pin is ')
  
        # subscribe mqtt
        self.mqtt.listen_event(self.wiegand_message, 'MQTT_MESSAGE', topic = 'wiegand/pin')
        self.mqtt.listen_event(self.wiegand_message, 'MQTT_MESSAGE', topic = 'wiegand/tag')
        self.mqtt.listen_event(self.wiegand_message, 'MQTT_MESSAGE', topic = 'wiegand/generatepin')
        self.log("App Started")
        #Setup motion, switch and daily callback functions
    #    self.set_state(self.auto_switch, state = "on")
    #    self.listen_state(self.switch, self.auto_switch)
        # self.listen_state(self.motion, self.motion_sensor_1, new = "on")
        
        #Initialise variables
        # self.turn_off(self.mq_light) 
        self.mqtt.mqtt_publish('wiegand/server/state', payload = "On", qos = 0, retain = True, namespace = "mqtt")
        # # self.mqtt.mqtt_publish(self.mq_light_color, payload = self.color_str(500,10), qos = 0, retain = True, namespace = "mqtt")    

    #    resultdata = self.database_select('PRAGMA table_info("wiegand_action")')        
    #    self.log("resuts : {}".format(resultdata))

    #    resultdata = self.database_select('SELECT * FROM wiegand_action')        
    #    self.log("resuts : {}".format(resultdata))

    #    resultdata = self.database_select('SELECT name FROM sqlite_master WHERE type="table"')        
    #    self.log("resuts : {}".format(resultdata))


    def wiegand_message(self, event_name, data, kwargs):
        topic = data['topic']
        payload = data['payload']
        self.log("{} payload: {}".format(topic, payload))

        if topic == 'wiegand/tag': 
            self.wiegand_tag(payload)
        
        if topic == 'wiegand/pin': 
            self.wiegand_pin(payload)

        if topic == 'wiegand/generatepin': 
            self.generate_pin(payload)
    

    def wiegand_pin(self,payload):
        payload_json = json.loads(payload)

        resultdata = self.database_select('SELECT id,state_text,error_counter_int FROM wiegand_reader WHERE reader_text = "{}"'.format(payload_json['reader']))

        if ( len(resultdata) <= 0):
            self.log("reader not exist : {}".format(payload_json['reader']))
            # TODO alarm unknown system
            return
        
        if (resultdata[0][1] == "L"):
            self.log("reader lock : {}  ignore input".format(payload_json['reader']))
            return

        if (resultdata[0][1] != "A"):
            self.log("reader disabled : {}  ignore input".format(payload_json['reader']))
            return

        reader_id = resultdata[0][0]
        reader_counter = resultdata[0][2]
        # Check PIN in database
        resultdata = self.database_select('SELECT pin_text,wiegand_pin.state_text,user_text,wiegand_pin.id FROM wiegand_pin,wiegand_user WHERE value_text = "{}" AND wiegand_pin.owner_id = wiegand_user.id '.format(payload_json['value']))

        if ( len(resultdata) > 0):
            self.log("pin {} presented on reader {}".format(resultdata[0][0],payload_json['reader']))
            if ( resultdata[0][1] == "A"):
                self.log("active pin ")
                self.reset_try_counter(reader_id)
                self.database_update('UPDATE wiegand_pin SET valid=1 WHERE id={}'.format(resultdata[0][3]))
                self.run_in(self.reset_valid_pin, 10, pin = resultdata[0][3] ) 
                self.check_trigger('pin',resultdata[0][3])
            else:
                self.log("unactive pin ")
                self.increase_try_counter(reader_id,reader_counter)
        else:
            self.log("unknown pin ")
            self.increase_try_counter(reader_id,reader_counter)

    def reset_valid_pin(self , kwargs ): 
        self.database_update('UPDATE wiegand_pin SET valid=0 WHERE id={}'.format(kwargs['pin']))


    def wiegand_tag(self,payload):
        payload_json = json.loads(payload)

        resultdata = self.database_select('SELECT id,state_text,error_counter_int FROM wiegand_reader WHERE reader_text = "{}"'.format(payload_json['reader']))

        if ( len(resultdata) <= 0):
            self.log("reader not exist : {}".format(payload_json['reader']))
            # TODO alarm unknown system
            return
        
        if (resultdata[0][1] == "L"):
            self.log("reader lock : {}  ignore input".format(payload_json['reader']))
            return

        if (resultdata[0][1] != "A"):
            self.log("reader disabled : {}  ignore input".format(payload_json['reader']))
            return

        reader_id = resultdata[0][0]
        reader_counter = resultdata[0][2]
        # Check TAG in database
        resultdata = self.database_select('SELECT tag_text,wiegand_tag.state_text,user_text,wiegand_tag.id FROM wiegand_tag,wiegand_user WHERE uid_text = "{}" AND wiegand_tag.owner_id = wiegand_user.id '.format(payload_json['value']))

        if ( len(resultdata) > 0):
            self.log("tag {} presented on reader {}".format(resultdata[0][0],payload_json['reader']))
            if ( resultdata[0][1] == "A"):
                self.log("active tag ")
                self.reset_try_counter(reader_id)
                self.database_update('UPDATE wiegand_tag SET valid=1 WHERE id={}'.format(resultdata[0][3]))
                self.run_in(self.reset_valid_tag, 10, tag = resultdata[0][3] ) 
                self.check_trigger('tag',resultdata[0][3])
            else:
                self.log("unactive tag ")
                self.increase_try_counter(reader_id,reader_counter)
        else:
            self.log("unknown tag ")
            self.increase_try_counter(reader_id,reader_counter)

    def reset_valid_tag(self , kwargs ): 
        self.database_update('UPDATE wiegand_tag SET valid=0 WHERE id={}'.format(kwargs['tag']))

    def reset_try_counter(self,reader):
        self.database_update('UPDATE wiegand_reader SET error_counter_int=0 WHERE id={}'.format(reader))

    def increase_try_counter(self,reader,reader_counter):
        newcounter = reader_counter + 1
        if ( newcounter > self.counter_limit ):
            self.database_update('UPDATE wiegand_reader SET error_counter_int={} , state_text="L" WHERE id={}'.format(newcounter,reader))
            self.run_in(self.reset_reader_lock, 60, reader = reader ) 
        else:
            self.database_update('UPDATE wiegand_reader SET error_counter_int={} WHERE id={}'.format(newcounter,reader))


    def check_trigger(self,triggertype,ojbid):

        if ( triggertype=='pin' ):
            resultdata = self.database_select('SELECT wiegand_trigger_conditions.trigger_id FROM wiegand_trigger_conditions,wiegand_condition WHERE wiegand_condition.associated_pin_id = {} AND wiegand_condition.id = wiegand_trigger_conditions.condition_id '.format(ojbid))        
            self.check_list_trigger(resultdata)
        elif ( triggertype=='tag' ):
            resultdata = self.database_select('SELECT wiegand_trigger_conditions.trigger_id FROM wiegand_trigger_conditions,wiegand_condition WHERE wiegand_condition.associated_tag_id = {} AND wiegand_condition.id = wiegand_trigger_conditions.condition_id '.format(ojbid))        
            self.check_list_trigger(resultdata)
        else:
            return

    def check_list_trigger(self , triggerlist):
        for trigg in triggerlist:
            # check all conditions of the trigger
            conditionok = 0  # 0 = nothing 1 = ok  2 = nok 
            resultdata = self.database_select('SELECT iftype,ifchain,associated_pin_id,associated_tag_id,associated_status_id FROM wiegand_condition, wiegand_trigger_conditions WHERE wiegand_condition.id = wiegand_trigger_conditions.condition_id AND wiegand_trigger_conditions.trigger_id = {}'.format(trigg[0]))        
            for condition in resultdata:
                subconditionok = False 
                self.log("condition : {}".format(condition))
                if ( condition[0] == 'T'):  #TYPE TAG 
                    subconditionok = self.check_tag_valid(condition[3])
                if ( condition[0] == 'P'):  #TYPE TAG 
                    subconditionok = self.check_pin_valid(condition[2])

                if ( condition[1] == 'O'):  #OR
                    if ( subconditionok ) :
                        conditionok = 1

                if ( condition[1] == 'A') | ( condition[3] == 'I'):  #AND or IF
                    if ( subconditionok ) & ( conditionok == 0) :
                        conditionok = 1
                    elif ( subconditionok ) & ( conditionok == 1) :
                        conditionok = 1
                    else:
                        conditionok = 2


            if ( conditionok == 1 ):
                self.log("condition succeed ")
                self.run_trigger_actions(trigg[0])

    def check_tag_valid(self,tagid):
        resultdata = self.database_select("SELECT valid FROM wiegand_tag WHERE id={}".format(tagid))
        if ( resultdata[0][0] == 1):
            return True
        return False

    def check_pin_valid(self,pinid):
        resultdata = self.database_select("SELECT valid FROM wiegand_pin WHERE id={}".format(pinid))
        if ( resultdata[0][0] == 1):
            return True
        return False


    def run_trigger_actions(self, triggerid):
        resultdata = self.database_select("SELECT action_id FROM wiegand_trigger_actions WHERE trigger_id={}".format(triggerid))
        for action in resultdata:
            self.run_action(action[0])
        return

    def run_action(self,actionid):
        actions = self.database_select("SELECT name_text,type_status,payload,topic FROM wiegand_action WHERE id={}".format(actionid))
        self.log("run action {}  ".format(actions[0][0]))
        if ( actions[0][1] == "M" ):
            self.mqtt.mqtt_publish(actions[0][3], payload = actions[0][2], qos = 0, retain = True, namespace = "mqtt")
        if ( actions[0][1] == "S" ):
            #{ "entity_id" : "light.bureau" }
            serviceparams = json.loads(actions[0][2])
            self.call_service("{}".format(actions[0][3]), **serviceparams)
        if ( actions[0][1] == "N" ):
            serviceparams = json.loads(actions[0][2])
            # { "title" : "Some Subject", "name" : "smtp" }
            self.notify("{}".format(actions[0][3]), **serviceparams)

    def generate_pin(self, notifyparam):
        newpin = randrange(self.pin_size)
        serviceparams = json.loads(notifyparam)
        pinid = serviceparams['pin_text']
        self.database_update('UPDATE wiegand_pin SET value_text="{}", state_text="A" WHERE pin_text={}'.format(newpin,pinid))
        self.notify("{} : {}".format(self.pin_message,newpin), **serviceparams)


    def reset_reader_lock(self, kwargs ): 
        self.database_update('UPDATE wiegand_reader SET state_text="A" WHERE id={}'.format(reader))

    def database_update(self,request):
        sqlDataBase = sqlite3.connect(self.sqlite_database)
        QueryCurs = sqlDataBase.cursor()
        QueryCurs.execute(request)
        sqlDataBase.commit()
        sqlDataBase.close()

    def database_select(self,request):
        sqlDataBase = sqlite3.connect(self.sqlite_database)
        QueryCurs = sqlDataBase.cursor()
        QueryCurs.execute(request)
        resultdata = QueryCurs.fetchall()
        sqlDataBase.close()
        return resultdata

    def save_mqtt(self, Mqtt):
        self.mqtt = Mqtt 
