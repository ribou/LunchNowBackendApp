import sys
from time import sleep
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import Twin, TwinProperties, QuerySpecification, QueryResult
from flask import Flask,render_template,request

IOTHUB_CONNECTION_STRING = [ ********** ] # Please replace by Azure IoT Hub Connection String. 
DEVICE_ID = [ ********** ] # Please replace by the name of Azure IoT Device

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main_page():
    if request.method == 'GET':
        text = "ここに結果が出力されます"
        return render_template("lunchNowPanel.html",text=text)
    elif request.method == 'POST':
        status = request.form["status"]
        text = "現在のステータスは" + status + "です"
        iothub_service_sample_run(status)
        return render_template("lunchNowPanel.html",text=text)

def iothub_service_sample_run(status):
    try:

        iothub_registry_manager = IoTHubRegistryManager(IOTHUB_CONNECTION_STRING)

        new_tags = {
                'location' : {
                    'region' : 'JP',
                    'plant' : 'Otemachi'
                }
            }

        twin = iothub_registry_manager.get_twin(DEVICE_ID)
        twin_patch = Twin(tags=new_tags, properties= TwinProperties(desired={'status' : int(status)}))
        twin = iothub_registry_manager.update_twin(DEVICE_ID, twin_patch, twin.etag)

        # Add a delay to account for any latency before executing the query
        sleep(1)

#        query_spec = QuerySpecification(query="SELECT * FROM devices WHERE tags.location.plant = 'Otemachi'")
#        query_result = iothub_registry_manager.query_iot_hub(query_spec, None, 100)
#        print("Devices in Otemachi plant: {}".format(', '.join([twin.device_id for twin in query_result.items])))

#        query_spec = QuerySpecification(query="SELECT * FROM devices WHERE tags.location.plant = 'Otemachi' AND properties.reported.connectivity = 'fixedline'")
#        query_result = iothub_registry_manager.query_iot_hub(query_spec, None, 100)
#        print("Devices in Otemachi plant using fixedline network: {}".format(', '.join([twin.device_id for twin in query_result.items])))

    except Exception as ex:
        print("Unexpected error {0}".format(ex))
        return
    except KeyboardInterrupt:
        print("IoT Hub Device Twin service sample stopped")

## 実行
if __name__ == "__main__":
    app.run(debug=True)
