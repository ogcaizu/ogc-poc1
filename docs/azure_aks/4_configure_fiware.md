# 4. configure fiware on AKS

Configure fiware on AKS by following steps:

1. [register "BUTTON-SENSOR" to cygnus](#register-button-sensor-to-cygnus)
1. [register "PEPPER" to cygnus](#register-pepper-to-cygnus)
1. [register "ROBOT" to cygnus](#register-robot-to-cygnus)
1. [register "CAMERA" to cygnus](#register-camera-to-cygnus)
1. [register "DEST-LED" to cygnus](#register-dest-led-to-cygnus)
1. [register "DEST-HUMAN-SENSOR" to cygnus](#register-dest-human-sensor-to-cygnus)
1. [register `start-reception` of "reception" as a subscriber of "BUTTON-SENSOR"](#register-start-reception-of-reception-as-a-subscriber-of-button-sensor)
1. [register `finish-reception` of "reception" as a subscriber of "PEPPER"](#register-finish-reception-of-reception-as-a-subscriber-of-pepper)
1. [register `record-reception` of "ledger" as a subscriber of "PEPPER"](#register-record-reception-of-ledger-as-a-subscriber-of-pepper)
1. [register `detect-visitor` of "ledger" as a subscriber of "PEPPER"](#register-detect-visitor-of-ledger-as-a-subscriber-of-pepper)
1. [register `reask-destination` of "ledger" as a subscriber of "PEPPER"](#register-reask-destination-of-ledger-as-a-subscriber-of-pepper)
1. [register `start_movement` entity](#register-stert_movement-entity)
1. [register `start-movement` of "guidance" as a subscriber of `start_movement`](#register-start-movement-of-guidance-as-a-subscriber-of-start_movement)
1. [register cygnus as as subscriber of `start_movement`](#register-cygnus-as-a-subscriber-of-start_movement)
1. [register `check-destination` of "guidance" as a subscriber of "ROBOT"](#register-check-destination-of-guidance-as-a-subscriber-of-robot)
1. [register `stop-movement` of "guidance" as a subscriber of "ROBOT"](#register-stop-movement-of-guidance-as-a-subscriber-of-robot)
1. [register `record-arrival` of "ledger" as a subscriber of "DEST-HUMAN-SENSOR"](#register-record-arrival-of-ledger-as-a-subscriber-of-dest-human-sensor)
1. [register `arrival` of "guidance" as a subscriber of "DEST-HUMAN-SENSOR"](#register-arrival-of-guidance-as-a-subscriber-of-dest-human-sensor)
1. [register desinations](#register-destinations)
1. [register "ROBOT" to cygnus-elasticseatch](#register-robot-to-cygnus-elasticsearch)

## register BUTTON-SENSOR to cygnus
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "button_sensor.*",
      "type": "button_sensor"
    }]
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5050/notify"
    },
    "attrs": ["state"],
    "attrsFormat": "legacy"
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b3c41f0d31a6404acc0ae2c",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "button_sensor.*",
          "type": "button_sensor"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-07-04T03:41:36.00Z",
      "attrs": [
        "state"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-07-04T03:41:36.00Z"
    }
  }
]
```
```bash
mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_button_sensor --eval 'db.getCollection("sth_/_button_sensor_0000000000000001_button_sensor").find().sort({recvTime: -1})'
MongoDB shell version v3.6.6
connecting to: mongodb://127.0.0.1:27017/sth_button_sensor
MongoDB server version: 3.6.6
{ "_id" : ObjectId("5bc5204501cf4c000b1c0951"), "recvTime" : ISODate("2018-10-15T23:18:29.046Z"), "state" : "on" }
```

# #register PEPPER to cygnus
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "pepper.*",
      "type": "pepper"
    }]
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5050/notify"
    },
    "attrs": ["dest", "face", "welcome_status", "handover_status", "facedetect_status", "reask_status"],
    "attrsFormat": "legacy"
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b3c43d4f1bdbe368d81d4c1",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "pepper.*",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-07-04T03:49:40.00Z",
      "attrs": [
        "dest",
        "face",
        "welcome_status",
        "handover_status",
        "facedetect_status",
        "reask_status"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-07-04T03:49:40.00Z"
    }
  }
]
```
```bash
$ kubectl exec mongodb-0 -c mongodb -- mongo sth_pepper --eval 'db.getCollection("sth_/_pepper_0000000000000001_pepper").find().sort({recvTime: -1})'
MongoDB shell version v3.6.6
connecting to: mongodb://127.0.0.1:27017/sth_pepper
MongoDB server version: 3.6.6
{ "_id" : ObjectId("5bc52508bcaa26000d22854e"), "recvTime" : ISODate("2018-10-15T23:38:46.374Z"), "dest" : "dest 1-1", "face" : "null", "facedetect_status" : "UNKNOWN", "handover_status" : "UNKNOWN", "reask_status" : "UNKNOWN", "welcome_status" : "OK" }
{ "_id" : ObjectId("5bc5249fbcaa26000d22854b"), "recvTime" : ISODate("2018-10-15T23:37:02.918Z"), "dest" : "dest 1-1", "face" : "null", "facedetect_status" : "UNKNOWN", "handover_status" : "UNKNOWN", "reask_status" : "UNKNOWN", "welcome_status" : "PENDING" }
```

## register ROBOT to cygnus
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "guide_robot.*",
      "type": "guide_robot"
    }]
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5050/notify"
    },
    "attrs": [
      "time",
      "r_mode",
      "x",
      "y",
      "theta",
      "r_state",
      "destx",
      "desty",
      "visitor",
      "robot_request_status",
      "robot_request_info"
    ],
    "attrsFormat": "legacy"
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b692eafbc0be89f5baac3d9",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "guide_robot.*",
          "type": "guide_robot"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-08-07T05:31:27.00Z",
      "attrs": [
        "time",
        "r_mode",
        "x",
        "y",
        "theta",
        "r_state",
        "destx",
        "desty",
        "visitor",
        "robot_request_status",
        "robot_request_info"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-08-07T05:31:27.00Z"
    }
  }
]
```
```bash
mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_robot --eval 'db.getCollection("sth_/_guide_robot_0000000000000001_guide_robot").find().sort({recvTime: -1})'
MongoDB shell version v3.6.6
connecting to: mongodb://127.0.0.1:27017/sth_robot
MongoDB server version: 3.6.6
d" : ObjectId("5bc5259301cf4c000b1c0956"), "recvTime" : ISODate("2018-10-15T23:41:07.753Z"), "destx" : "20.0", "desty" : "-10.8", "r_mode" : "Navi", "r_state" : "Guiding", "robot_request_info" : "result,success/time,2018-10-16 08:37:02/r_cmd,Navi/x,20.0/y,-10.8", "robot_request_status" : "OK", "theta" : "0.3", "time" : "2018-09-08 07:06:05", "visitor" : "bxA21JOPcNhyQr0YqylCaqXV", "x" : "0.1", "y" : "0.2" }
```
```bash
mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_robot --eval 'db.getCollection("sth_/_guide_robot_0000000000000002_guide_robot").find().sort({recvTime: -1})'
MongoDB shell version v3.6.6
connecting to: mongodb://127.0.0.1:27017/sth_robot
MongoDB server version: 3.6.6
{ "_id" : ObjectId("5bc52b0f8e39fa000e14fae8"), "recvTime" : ISODate("2018-10-16T00:04:27.063Z"), "destx" : "20.0", "desty" : "20.0", "r_mode" : "Navi", "r_state" : "Guiding", "robot_request_info" : "result,success/time,2018-10-16 09:04:27/r_cmd,Navi/x,20.0/y,20.0", "robot_request_status" : "OK", "theta" : "0.3", "time" : "2018-Oct-10 12:47:04.098249", "visitor" : "5bc52a9469104a0016f66dac", "x" : "0.1", "y" : "0.2" }
```

## register CAMERA to cygnus

```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: camera" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "external_camera.*",
      "type": "external_camera"
    }]
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5050/notify"
    },
    "attrs": [
      "time",
      "c_mode",
      "num_p",
      "position",
      "external_camera_request_status",
      "external_camera_request_info"
    ],
    "attrsFormat": "legacy"
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: camera" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b60fbaabc0be89f5baac3d2",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "external_camera.*",
          "type": "external_camera"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-08-01T00:15:38.00Z",
      "attrs": [
        "time",
        "c_mode",
        "num_p",
        "position",
        "external_camera_request_status",
        "external_camera_request_info"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-08-01T00:15:38.00Z"
    }
  }
]
```
```bash
mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_camera --eval 'db.getCollection("sth_/_external_camera_0000000000000011_external_camera").find().sort({recvTime: -1})'
MongoDB shell version v3.6.6
connecting to: mongodb://127.0.0.1:27017/sth_camera
MongoDB server version: 3.6.6
{ "_id" : ObjectId("5bbc5dbebcaa26000d22797f"), "recvTime" : ISODate("2018-10-09T07:50:22.630Z"), "c_mode" : "Monitor", "external_camera_request_info" : "result,success/time,2018-10-09 15:30:59/c_cmd,Monitor", "external_camera_request_status" : "OK", "num_p" : "1", "position" : "x[0],1.12/y[0],-95.1", "time" : "2018-01-02 03:04:05" }
```
```bash
mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_camera --eval 'db.getCollection("sth_/_external_camera_0000000000000012_external_camera").find().sort({recvTime: -1})'
MongoDB shell version v3.6.6
connecting to: mongodb://127.0.0.1:27017/sth_camera
MongoDB server version: 3.6.6
{ "_id" : ObjectId("5bbc5dbf01cf4c000b1bfd3d"), "recvTime" : ISODate("2018-10-09T07:50:23.772Z"), "c_mode" : "Monitor", "external_camera_request_info" : "result,success/time,2018-10-09 15:31:31/c_cmd,Monitor", "external_camera_request_status" : "OK", "num_p" : "0", "position" : "-", "time" : "2018-01-02 03:04:05" }
```
```bash
mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_camera --eval 'db.getCollection("sth_/_external_camera_0000000000000021_external_camera").find().sort({recvTime: -1})'
MongoDB shell version v3.6.6
connecting to: mongodb://127.0.0.1:27017/sth_camera
MongoDB server version: 3.6.6
{ "_id" : ObjectId("5bbc5dc2bcaa26000d227982"), "recvTime" : ISODate("2018-10-09T07:50:26.602Z"), "c_mode" : "Monitor", "external_camera_request_info" : "result,success/time,2018-10-09 15:31:42/c_cmd,Monitor", "external_camera_request_status" : "OK", "num_p" : "0", "position" : "-", "time" : "2018-01-02 03:04:05" }
```

## register DEST-LED to cygnus
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_led" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "dest_led.*",
      "type": "dest_led"
    }]
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5050/notify"
    },
    "attrs": ["action_status", "action_info"],
    "attrsFormat": "legacy"
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_led" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b3c83f2d31a6404acc0ae2f",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "dest_led.*",
          "type": "dest_led"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-07-04T08:23:14.00Z",
      "attrs": [
        "action_status",
        "action_info"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-07-04T08:23:14.00Z"
    }
  }
]
```
```bash
mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_dest_led --eval 'db.getCollection("sth_/_dest_led_0000000000000001_dest_led").find().sort({recvTime: -1})'
MongoDB shell version v3.6.6
connecting to: mongodb://127.0.0.1:27017/sth_dest_led
MongoDB server version: 3.6.6
{ "_id" : ObjectId("5bc5267c8e39fa000e14fae5"), "recvTime" : ISODate("2018-10-15T23:45:00.920Z"), "action_info" : "success", "action_status" : "OK" }
{ "_id" : ObjectId("5bc5264cbcaa26000d228550"), "recvTime" : ISODate("2018-10-15T23:44:12.182Z"), "action_info" : "success", "action_status" : "PENDING" }
```

## register DEST-HUMAN-SENSOR to cygnus
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_human_sensor" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "dest_human_sensor.*",
      "type": "dest_human_sensor"
    }]
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5050/notify"
    },
    "attrs": ["arrival"],
    "attrsFormat": "legacy"
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_human_sensor" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b3d786bd31a6404acc0ae31",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "dest_human_sensor.*",
          "type": "dest_human_sensor"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-07-05T01:46:19.00Z",
      "attrs": [
        "arrival"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-07-05T01:46:19.00Z"
    }
  }
]
```
```bash
mac:$ kubectl exec mongodb-0 -c mongodb -- mongo sth_dest_human_sensor --eval 'db.getCollection("sth_/_dest_human_sensor_0000000000000001_dest_human_sensor").find().sort({recvTime: -1})'
MongoDB shell version v3.6.6
connecting to: mongodb://127.0.0.1:27017/sth_dest_human_sensor
MongoDB server version: 3.6.6
{ "_id" : ObjectId("5bc5264c01cf4c000b1c095a"), "recvTime" : ISODate("2018-10-15T23:44:12.133Z"), "arrival" : "2018-10-16T08:44:11.1539647051+0900" }
```

## register `start-reception` of reception as a subscriber of BUTTON-SENSOR
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "button_sensor.*",
      "type": "button_sensor"
    }],
    "condition": {
      "attrs": ["state"]
    }
  },
  "notification": {
    "http": {
      "url": "http://reception:8888/notify/start-reception/"
    },
    "attrs": ["state"]
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: button_sensor" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b358ed7cabb3e96b43251ba",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "button_sensor.*",
          "type": "button_sensor"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-06-29T01:43:51.00Z",
      "attrs": [
        "state"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-06-29T01:43:51.00Z"
    }
  },
  {
    "id": "5b35932607f08f3a3ac62b59",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "button_sensor.*",
          "type": "button_sensor"
        }
      ],
      "condition": {
        "attrs": [
          "state"
        ]
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-06-29T02:02:14.00Z",
      "attrs": [
        "state"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://reception:8888/notify/start-reception/"
      },
      "lastSuccess": "2018-06-29T02:02:14.00Z"
    }
  }
]
```

## register `finish-reception` of reception as a subscriber of PEPPER
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "id": "pepper_0000000000000001",
      "type": "pepper"
    }],
    "condition": {
      "attrs": ["face", "dest"]
    }
  },
  "notification": {
    "http": {
      "url": "http://reception:8888/notify/finish-reception/"
    },
    "attrs": ["face", "dest"]
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b3590a707f08f3a3ac62b58",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "pepper.*",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 6,
      "lastNotification": "2018-06-29T02:02:14.00Z",
      "attrs": [
        "dest",
        "face",
        "welcome_status",
        "handover_status",
        "facedetect_status",
        "reask_status"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-06-29T02:02:14.00Z"
    }
  },
  {
    "id": "5b35935fcabb3e96b43251bb",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "pepper_0000000000000001",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": [
          "face",
          "dest"
        ]
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-06-29T02:03:11.00Z",
      "attrs": [
        "face",
        "dest"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://reception:8888/notify/finish-reception/"
      },
      "lastSuccess": "2018-06-29T02:03:11.00Z"
    }
  }
]
```

## register `record-reception` of ledger as a subscriber of PEPPER
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "id": "pepper_0000000000000001",
      "type": "pepper"
    }],
    "condition": {
      "attrs": ["face", "dest"]
    }
  },
  "notification": {
    "http": {
      "url": "http://ledger:8888/notify/record-reception/"
    },
    "attrs": ["face", "dest"]
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b3590a707f08f3a3ac62b58",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "pepper.*",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 6,
      "lastNotification": "2018-06-29T02:02:14.00Z",
      "attrs": [
        "dest",
        "face",
        "welcome_status",
        "handover_status",
        "facedetect_status",
        "reask_status"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-06-29T02:02:14.00Z"
    }
  },
  {
    "id": "5b35935fcabb3e96b43251bb",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "pepper_0000000000000001",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": [
          "face",
          "dest"
        ]
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-06-29T02:03:11.00Z",
      "attrs": [
        "face",
        "dest"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://reception:8888/notify/finish-reception/"
      },
      "lastSuccess": "2018-06-29T02:03:11.00Z"
    }
  },
  {
    "id": "5b35944007f08f3a3ac62b5a",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "pepper_0000000000000001",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": [
          "face",
          "dest"
        ]
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-06-29T02:06:56.00Z",
      "attrs": [
        "face",
        "dest"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://ledger:8888/notify/record-reception/"
      }
    }
  }
]
```

## register `detect-visitor` of ledger as a subscriber of PEPPER
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "id": "pepper_0000000000000002",
      "type": "pepper"
    }],
    "condition": {
      "attrs": ["face"]
    }
  },
  "notification": {
    "http": {
      "url": "http://ledger:8888/notify/detect-visitor/"
    },
    "attrs": ["face"]
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b397c2c01ed8ed56809d2c8",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "pepper.*",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 36,
      "lastNotification": "2018-07-03T05:34:29.00Z",
      "attrs": [
        "dest",
        "face",
        "welcome_status",
        "handover_status",
        "facedetect_status",
        "reask_status"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-07-03T05:34:29.00Z"
    }
  },
  {
    "id": "5b397c967da87a300178826f",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "pepper_0000000000000001",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": [
          "face",
          "dest"
        ]
      }
    },
    "notification": {
      "timesSent": 14,
      "lastNotification": "2018-07-03T05:34:29.00Z",
      "attrs": [
        "face",
        "dest"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://reception:8888/notify/finish-reception/"
      },
      "lastSuccess": "2018-07-03T05:34:29.00Z"
    }
  },
  {
    "id": "5b397cac7da87a3001788270",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "pepper_0000000000000001",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": [
          "face",
          "dest"
        ]
      }
    },
    "notification": {
      "timesSent": 14,
      "lastNotification": "2018-07-03T05:34:29.00Z",
      "attrs": [
        "face",
        "dest"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://ledger:8888/notify/record-reception/"
      },
      "lastSuccess": "2018-07-03T05:34:29.00Z"
    }
  },
  {
    "id": "5b3ecfacd31a6404acc0ae36",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "pepper_0000000000000002",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": [
          "face"
        ]
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-07-06T02:10:52.00Z",
      "attrs": [
        "face"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://ledger:8888/notify/detect-visitor/"
      },
      "lastSuccess": "2018-07-06T02:10:52.00Z"
    }
  }
]
```

## register `reask-destination` of ledger as a subscriber of PEPPER
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "id": "pepper_0000000000000002",
      "type": "pepper"
    }],
    "condition": {
      "attrs": ["dest"]
    }
  },
  "notification": {
    "http": {
      "url": "http://ledger:8888/notify/reask-destination/"
    },
    "attrs": ["dest"]
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: pepper" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b397c2c01ed8ed56809d2c8",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "pepper.*",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 36,
      "lastNotification": "2018-07-03T05:34:29.00Z",
      "attrs": [
        "dest",
        "face",
        "welcome_status",
        "handover_status",
        "facedetect_status",
        "reask_status"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-07-03T05:34:29.00Z"
    }
  },
  {
    "id": "5b397c967da87a300178826f",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "pepper_0000000000000001",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": [
          "face",
          "dest"
        ]
      }
    },
    "notification": {
      "timesSent": 14,
      "lastNotification": "2018-07-03T05:34:29.00Z",
      "attrs": [
        "face",
        "dest"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://reception:8888/notify/finish-reception/"
      },
      "lastSuccess": "2018-07-03T05:34:29.00Z"
    }
  },
  {
    "id": "5b397cac7da87a3001788270",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "pepper_0000000000000001",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": [
          "face",
          "dest"
        ]
      }
    },
    "notification": {
      "timesSent": 14,
      "lastNotification": "2018-07-03T05:34:29.00Z",
      "attrs": [
        "face",
        "dest"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://ledger:8888/notify/record-reception/"
      },
      "lastSuccess": "2018-07-03T05:34:29.00Z"
    }
  },
  {
    "id": "5b3ecfacd31a6404acc0ae36",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "pepper_0000000000000002",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": [
          "face"
        ]
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-07-06T02:10:52.00Z",
      "attrs": [
        "face"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://ledger:8888/notify/detect-visitor/"
      },
      "lastSuccess": "2018-07-06T02:10:52.00Z"
    }
  },
  {
    "id": "5b3ed0b0f1bdbe368d81d4ce",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "pepper_0000000000000002",
          "type": "pepper"
        }
      ],
      "condition": {
        "attrs": [
          "dest"
        ]
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-07-06T02:15:12.00Z",
      "attrs": [
        "dest"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://ledger:8888/notify/reask-destination/"
      }
    }
  }
]
```

## register `start_movement` entity
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: start_movement" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/entities/ -X POST -d @- <<__EOS__
{
  "id": "start_movement",
  "type": "start_movement",
  "destx": {
    "type": "float",
    "value": "",
    "metadata": {}
  },
  "desty": {
    "type": "float",
    "value": "",
    "metadata": {}
  },
  "floor": {
    "type": "int",
    "value": "",
    "metadata": {}
  },
  "timestamp": {
    "type": "string",
    "value": "",
    "metadata": {}
  },
  "visitor_id": {
    "type": "string",
    "value": "",
    "metadata": {}
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: start_movement" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/entities/start_movement/ | jq .
{
  "id": "start_movement",
  "type": "start_movement",
  "destx": {
    "type": "float",
    "value": "",
    "metadata": {}
  },
  "desty": {
    "type": "float",
    "value": "",
    "metadata": {}
  },
  "floor": {
    "type": "int",
    "value": "",
    "metadata": {}
  },
  "timestamp": {
    "type": "string",
    "value": "",
    "metadata": {}
  },
  "visitor_id": {
    "type": "string",
    "value": "",
    "metadata": {}
  }
}
```

## register `start-movement` of guidance as a subscriber of `start_movement`
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: start_movement" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "id": "start_movement",
      "type": "start_movement"
    }],
    "condition": {
      "attrs": ["destx", "desty", "floor", "timestamp", "visitor_id"]
    }
  },
  "notification": {
    "http": {
      "url": "http://guidance:8888/notify/start-movement/"
    },
    "attrs": ["destx", "desty", "floor", "timestamp", "visitor_id"]
  }
}
__EOS__
```

## register cygnus as as subscriber of `start_movement`
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: start_movement" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "id": "start_movement",
      "type": "start_movement"
    }]
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5050/notify"
    },
    "attrs": ["destx", "desty", "floor", "timestamp", "visitor_id"],
    "attrsFormat": "legacy"
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: start_movement" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b694bffbc0be89f5baac3dc",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "start_movement",
          "type": "start_movement"
        }
      ],
      "condition": {
        "attrs": [
          "destx",
          "desty",
          "floor",
          "timestamp",
          "visitor_id"
        ]
      }
    },
    "notification": {
      "attrs": [
        "destx",
        "desty",
        "floor",
        "timestamp",
        "visitor_id"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://guidance:8888/notify/start-movement/"
      }
    }
  },
  {
    "id": "5b694c06bc0be89f5baac3dd",
    "status": "active",
    "subject": {
      "entities": [
        {
          "id": "start_movement",
          "type": "start_movement"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-08-07T07:36:38.00Z",
      "attrs": [
        "destx",
        "desty",
        "floor",
        "timestamp",
        "visitor_id"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-08-07T07:36:38.00Z"
    }
  }
]
```

## register `check-destination` of guidance as a subscriber of ROBOT
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "guide_robot.*",
      "type": "guide_robot"
    }],
    "condition": {
      "attrs": ["r_mode", "x", "y", "theta"],
      "expression": {
        "q": "r_mode==Navi"
      }
    }
  },
  "notification": {
    "http": {
      "url": "http://guidance:8888/notify/check-destination/"
    },
    "attrs": ["r_mode", "x", "y", "theta", "r_state", "destx", "desty", "visitor"]
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b692eafbc0be89f5baac3d9",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "guide_robot.*",
          "type": "guide_robot"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 4,
      "lastNotification": "2018-08-07T05:35:47.00Z",
      "attrs": [
        "time",
        "r_mode",
        "x",
        "y",
        "theta",
        "r_state",
        "destx",
        "desty",
        "visitor",
        "robot_request_status",
        "robot_request_info"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-08-07T05:35:47.00Z"
    }
  },
  {
    "id": "5b69302bbc0be89f5baac3da",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "guide_robot.*",
          "type": "guide_robot"
        }
      ],
      "condition": {
        "attrs": [
          "r_mode",
          "x",
          "y",
          "theta"
        ],
        "expression": {
          "q": "r_mode==Navi"
        }
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-08-07T05:37:47.00Z",
      "attrs": [
        "r_mode",
        "x",
        "y",
        "theta",
        "r_state",
        "destx",
        "desty",
        "visitor"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://guidance:8888/notify/check-destination/"
      }
    }
  }
]
```

## register `stop-movement` of guidance as a subscriber of ROBOT
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "guide_robot.*",
      "type": "guide_robot"
    }],
    "condition": {
      "attrs": ["r_mode", "x", "y", "theta"],
      "expression": {
        "q": "r_mode==Standby"
      }
    }
  },
  "notification": {
    "http": {
      "url": "http://guidance:8888/notify/stop-movement/"
    },
    "attrs": ["r_mode", "x", "y", "theta", "r_state", "destx", "desty", "visitor"]
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b692eafbc0be89f5baac3d9",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "guide_robot.*",
          "type": "guide_robot"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 4,
      "lastNotification": "2018-08-07T05:35:47.00Z",
      "attrs": [
        "time",
        "r_mode",
        "x",
        "y",
        "theta",
        "r_state",
        "destx",
        "desty",
        "visitor",
        "robot_request_status",
        "robot_request_info"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-08-07T05:35:47.00Z"
    }
  },
  {
    "id": "5b69302bbc0be89f5baac3da",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "guide_robot.*",
          "type": "guide_robot"
        }
      ],
      "condition": {
        "attrs": [
          "r_mode",
          "x",
          "y",
          "theta"
        ],
        "expression": {
          "q": "r_mode==Navi"
        }
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-08-07T05:37:47.00Z",
      "attrs": [
        "r_mode",
        "x",
        "y",
        "theta",
        "r_state",
        "destx",
        "desty",
        "visitor"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://guidance:8888/notify/check-destination/"
      },
      "lastSuccess": "2018-08-07T05:37:47.00Z"
    }
  },
  {
    "id": "5b69308bbc0be89f5baac3db",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "guide_robot.*",
          "type": "guide_robot"
        }
      ],
      "condition": {
        "attrs": [
          "r_mode",
          "x",
          "y",
          "theta"
        ],
        "expression": {
          "q": "r_mode==Standby"
        }
      }
    },
    "notification": {
      "attrs": [
        "r_mode",
        "x",
        "y",
        "theta",
        "r_state",
        "destx",
        "desty",
        "visitor"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://guidance:8888/notify/stop-movement/"
      }
    }
  }
]
```

## register `change-robot-state` of guidance as a subscriber of ROBOT
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "guide_robot.*",
      "type": "guide_robot"
    }],
    "condition": {
      "attrs": ["r_state"]
    }
  },
  "notification": {
    "http": {
      "url": "http://guidance:8888/notify/change-robot-state/"
    },
    "attrs": ["r_state"]
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b723fc3cce8da6ea14fd67f",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "guide_robot.*",
          "type": "guide_robot"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 14544,
      "lastNotification": "2018-10-16T00:46:40.00Z",
      "attrs": [
        "time",
        "r_mode",
        "x",
        "y",
        "theta",
        "r_state",
        "destx",
        "desty",
        "visitor",
        "robot_request_status",
        "robot_request_info"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-10-16T00:46:40.00Z"
    }
  },
  {
    "id": "5b7240e3cce8da6ea14fd683",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "guide_robot.*",
          "type": "guide_robot"
        }
      ],
      "condition": {
        "attrs": [
          "r_mode",
          "x",
          "y",
          "theta"
        ],
        "expression": {
          "q": "r_mode==Navi"
        }
      }
    },
    "notification": {
      "timesSent": 2788,
      "lastNotification": "2018-10-15T23:41:07.00Z",
      "attrs": [
        "r_mode",
        "x",
        "y",
        "theta",
        "r_state",
        "destx",
        "desty",
        "visitor"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://guidance:8888/notify/check-destination/"
      },
      "lastFailure": "2018-10-10T01:30:58.00Z",
      "lastSuccess": "2018-10-15T23:41:07.00Z"
    }
  },
  {
    "id": "5b7240f5cce8da6ea14fd684",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "guide_robot.*",
          "type": "guide_robot"
        }
      ],
      "condition": {
        "attrs": [
          "r_mode",
          "x",
          "y",
          "theta"
        ],
        "expression": {
          "q": "r_mode==Standby"
        }
      }
    },
    "notification": {
      "timesSent": 11244,
      "lastNotification": "2018-10-16T00:11:48.00Z",
      "attrs": [
        "r_mode",
        "x",
        "y",
        "theta",
        "r_state",
        "destx",
        "desty",
        "visitor"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://guidance:8888/notify/stop-movement/"
      },
      "lastFailure": "2018-10-10T01:33:23.00Z",
      "lastSuccess": "2018-10-16T00:11:48.00Z"
    }
  },
  {
    "id": "5bc535fa1797ff091b693505",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "guide_robot.*",
          "type": "guide_robot"
        }
      ],
      "condition": {
        "attrs": [
          "r_state"
        ]
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-10-16T00:51:06.00Z",
      "attrs": [
        "r_state"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://guidance:8888/notify/change-robot-state/"
      },
      "lastSuccess": "2018-10-16T00:51:06.00Z"
    }
  }
]
```

## register `record-arrival` of ledger as a subscriber of DEST-HUMAN-SENSOR
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_human_sensor" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "dest_human_sensor.*",
      "type": "dest_human_sensor"
    }],
    "condition": {
      "attrs": ["arrival"]
    }
  },
  "notification": {
    "http": {
      "url": "http://ledger:8888/notify/record-arrival/"
    },
    "attrs": ["arrival"]
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_human_sensor" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b3d786bd31a6404acc0ae31",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "dest_human_sensor.*",
          "type": "dest_human_sensor"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 3,
      "lastNotification": "2018-07-05T02:53:34.00Z",
      "attrs": [
        "arrival"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-07-05T02:53:34.00Z"
    }
  },
  {
    "id": "5b3d8959d31a6404acc0ae32",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "dest_human_sensor.*",
          "type": "dest_human_sensor"
        }
      ],
      "condition": {
        "attrs": [
          "arrival"
        ]
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-07-05T02:58:33.00Z",
      "attrs": [
        "arrival"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://ledger:8888/notify/record-arrival/"
      },
      "lastSuccess": "2018-07-05T02:58:33.00Z"
    }
  }
]
```

## register `arrival` of guidance as a subscriber of DEST-HUMAN-SENSOR
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_human_sensor" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "dest_human_sensor.*",
      "type": "dest_human_sensor"
    }],
    "condition": {
      "attrs": ["arrival"]
    }
  },
  "notification": {
    "http": {
      "url": "http://guidance:8888/notify/arrival/"
    },
    "attrs": ["arrival"]
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: dest_human_sensor" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b3d786bd31a6404acc0ae31",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "dest_human_sensor.*",
          "type": "dest_human_sensor"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 5,
      "lastNotification": "2018-07-05T03:34:44.00Z",
      "attrs": [
        "arrival"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastSuccess": "2018-07-05T03:34:44.00Z"
    }
  },
  {
    "id": "5b3d8959d31a6404acc0ae32",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "dest_human_sensor.*",
          "type": "dest_human_sensor"
        }
      ],
      "condition": {
        "attrs": [
          "arrival"
        ]
      }
    },
    "notification": {
      "timesSent": 3,
      "lastNotification": "2018-07-05T03:34:44.00Z",
      "attrs": [
        "arrival"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://ledger:8888/notify/record-arrival/"
      },
      "lastSuccess": "2018-07-05T03:34:44.00Z"
    }
  },
  {
    "id": "5b3d921ad31a6404acc0ae33",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "dest_human_sensor.*",
          "type": "dest_human_sensor"
        }
      ],
      "condition": {
        "attrs": [
          "arrival"
        ]
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-07-05T03:35:54.00Z",
      "attrs": [
        "arrival"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://guidance:8888/notify/arrival/"
      },
      "lastSuccess": "2018-07-05T03:35:54.00Z"
    }
  }
]
```

## register destinations
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl https://api.tech-sketch.jp/destinations/ -H "Authorization: bearer ${TOKEN}" -H "Content-Type: application/json" -X POST -d @- <<__EOS__ | jq .
{
    "name":"initial-1",
    "floor": 1,
    "dest_pos_x": 0.0,
    "dest_pos_y": 0.0,
    "dest_led_id": null,
    "dest_led_pos_x": null,
    "dest_led_pos_y": null,
    "dest_human_sensor_id": null,
    "initial": true
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl https://api.tech-sketch.jp/destinations/ -H "Authorization: bearer ${TOKEN}" -H "Content-Type: application/json" -X POST -d @- <<__EOS__ | jq .
{
    "name":"initial-2",
    "floor": 2,
    "dest_pos_x": 0.0,
    "dest_pos_y": 0.0,
    "dest_led_id": null,
    "dest_led_pos_x": null,
    "dest_led_pos_y": null,
    "dest_human_sensor_id": null,
    "initial": true
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl https://api.tech-sketch.jp/destinations/ -H "Authorization: bearer ${TOKEN}" -H "Content-Type: application/json" -X POST -d @- <<__EOS__ | jq .
{
    "name":"dest 1-1",
    "floor": 1,
    "dest_pos_x": -12.388,
    "dest_pos_y": 7.51,
    "dest_led_id": "dest_led_0000000000000001",
    "dest_led_pos_x": -8.388,
    "dest_led_pos_y": 7.51,
    "dest_human_sensor_id": "dest_human_sensor_0000000000000001"
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl https://api.tech-sketch.jp/destinations/ -H "Authorization: bearer ${TOKEN}" -H "Content-Type: application/json" -X POST -d @- <<__EOS__ | jq .
{
    "name":"dest 2-1",
    "floor": 2,
    "dest_pos_x": 11.642,
    "dest_pos_y": 0,
    "dest_led_id": "dest_led_0000000000000002",
    "dest_led_pos_x": 7.642,
    "dest_led_pos_y": 0,
    "dest_human_sensor_id": "dest_human_sensor_0000000000000002"
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl https://api.tech-sketch.jp/destinations/ -H "Authorization: bearer ${TOKEN}" -H "Content-Type: application/json" -X POST -d @- <<__EOS__ | jq .
{
    "name":"ProjectRoom 1",
    "floor": 3,
    "dest_pos_x": null,
    "dest_pos_y": null,
    "dest_led_id": null,
    "dest_led_pos_x": null,
    "dest_led_pos_y": null,
    "dest_human_sensor_id": null,
    "slack_webhook": "https://hooks.slack.com/services/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}
__EOS__
```
```bash
TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl https://api.tech-sketch.jp/destinations/ -H "Authorization: bearer ${TOKEN}" -H "Content-Type: application/json" -X POST -d @- <<__EOS__ | jq .
{
    "name":"dest 1-2",
    "floor": 1,
    "dest_pos_x": -10.68,
    "dest_pos_y": 7.51,
    "dest_led_id": "dest_led_0000000000000003",
    "dest_led_pos_x": -6.68,
    "dest_led_pos_y": 7.51,
    "dest_human_sensor_id": "dest_human_sensor_0000000000000003"
}
__EOS__
```
```bash
TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl https://api.tech-sketch.jp/destinations/ -H "Authorization: bearer ${TOKEN}" -H "Content-Type: application/json" -X POST -d @- <<__EOS__ | jq .
{
    "name":"dest 1-3",
    "floor": 1,
    "dest_pos_x": -9.58,
    "dest_pos_y": 7.51,
    "dest_led_id": "dest_led_0000000000000004",
    "dest_led_pos_x": -5.58,
    "dest_led_pos_y": 7.51,
    "dest_human_sensor_id": "dest_human_sensor_0000000000000004"
}
__EOS__
```
```bash
TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl https://api.tech-sketch.jp/destinations/ -H "Authorization: bearer ${TOKEN}" -H "Content-Type: application/json" -X POST -d @- <<__EOS__ | jq .
{
    "name":"dest 1-4",
    "floor": 1,
    "dest_pos_x": -6.41,
    "dest_pos_y": 7.51,
    "dest_led_id": "dest_led_0000000000000005",
    "dest_led_pos_x": -2.41,
    "dest_led_pos_y": 7.51,
    "dest_human_sensor_id": "dest_human_sensor_0000000000000005"
}
__EOS__
```
```bash
TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl https://api.tech-sketch.jp/destinations/ -H "Authorization: bearer ${TOKEN}" -H "Content-Type: application/json" -X POST -d @- <<__EOS__ | jq .
{
    "name":"dest 2-2",
    "floor": 2,
    "dest_pos_x": 15.325,
    "dest_pos_y": 0,
    "dest_led_id": "dest_led_0000000000000006",
    "dest_led_pos_x": 11.325,
    "dest_led_pos_y": 0,
    "dest_human_sensor_id": "dest_human_sensor_0000000000000006"
}
__EOS__
```
```bash
TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl https://api.tech-sketch.jp/destinations/ -H "Authorization: bearer ${TOKEN}" -H "Content-Type: application/json" -X POST -d @- <<__EOS__ | jq .
{
    "name":"dest 2-3",
    "floor": 2,
    "dest_pos_x": 18.72,
    "dest_pos_y": 0,
    "dest_led_id": "dest_led_0000000000000007",
    "dest_led_pos_x": 14.72,
    "dest_led_pos_y": 0,
    "dest_human_sensor_id": "dest_human_sensor_0000000000000007"
}
__EOS__
```

## register ROBOT to cygnus-elasticsearch
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-ServicePath: /" -H "Content-Type: application/json" https://api.tech-sketch.jp/orion/v2/subscriptions/ -X POST -d @- <<__EOS__
{
  "subject": {
    "entities": [{
      "idPattern": "guide_robot.*",
      "type": "guide_robot"
    }],
    "condition": {
      "attrs": ["time", "r_mode", "x", "y", "theta", "r_state"]
    }
  },
  "notification": {
    "http": {
      "url": "http://cygnus-elasticsearch:5050/notify"
    },
    "attrs": [
      "time",
      "r_mode",
      "x",
      "y",
      "theta",
      "r_state"
    ],
    "attrsFormat": "legacy"
  }
}
__EOS__
```
```bash
mac:$ TOKEN=$(cat secrets/auth-tokens.json | jq '.bearer_tokens[0].token' -r);curl -sS -H "Authorization: bearer ${TOKEN}" -H "Fiware-Service: robot" -H "Fiware-ServicePath: /" https://api.tech-sketch.jp/orion/v2/subscriptions/ | jq .
[
  {
    "id": "5b723fc3cce8da6ea14fd67f",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "guide_robot.*",
          "type": "guide_robot"
        }
      ],
      "condition": {
        "attrs": []
      }
    },
    "notification": {
      "timesSent": 14704,
      "lastNotification": "2018-10-22T01:32:41.00Z",
      "attrs": [
        "time",
        "r_mode",
        "x",
        "y",
        "theta",
        "r_state",
        "destx",
        "desty",
        "visitor",
        "robot_request_status",
        "robot_request_info"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus:5050/notify"
      },
      "lastFailure": "2018-10-22T01:32:35.00Z",
      "lastSuccess": "2018-10-22T01:32:41.00Z"
    }
  },
  {
    "id": "5b7240e3cce8da6ea14fd683",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "guide_robot.*",
          "type": "guide_robot"
        }
      ],
      "condition": {
        "attrs": [
          "r_mode",
          "x",
          "y",
          "theta"
        ],
        "expression": {
          "q": "r_mode==Navi"
        }
      }
    },
    "notification": {
      "timesSent": 2792,
      "lastNotification": "2018-10-16T05:07:19.00Z",
      "attrs": [
        "r_mode",
        "x",
        "y",
        "theta",
        "r_state",
        "destx",
        "desty",
        "visitor"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://guidance:8888/notify/check-destination/"
      },
      "lastFailure": "2018-10-10T01:30:58.00Z",
      "lastSuccess": "2018-10-16T05:07:19.00Z"
    }
  },
  {
    "id": "5b7240f5cce8da6ea14fd684",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "guide_robot.*",
          "type": "guide_robot"
        }
      ],
      "condition": {
        "attrs": [
          "r_mode",
          "x",
          "y",
          "theta"
        ],
        "expression": {
          "q": "r_mode==Standby"
        }
      }
    },
    "notification": {
      "timesSent": 11260,
      "lastNotification": "2018-10-18T07:20:14.00Z",
      "attrs": [
        "r_mode",
        "x",
        "y",
        "theta",
        "r_state",
        "destx",
        "desty",
        "visitor"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://guidance:8888/notify/stop-movement/"
      },
      "lastFailure": "2018-10-10T01:33:23.00Z",
      "lastSuccess": "2018-10-18T07:20:15.00Z"
    }
  },
  {
    "id": "5bc535fa1797ff091b693505",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "guide_robot.*",
          "type": "guide_robot"
        }
      ],
      "condition": {
        "attrs": [
          "r_state"
        ]
      }
    },
    "notification": {
      "timesSent": 80,
      "lastNotification": "2018-10-22T01:32:41.00Z",
      "attrs": [
        "r_state"
      ],
      "attrsFormat": "normalized",
      "http": {
        "url": "http://guidance:8888/notify/change-robot-state/"
      },
      "lastSuccess": "2018-10-22T01:32:41.00Z"
    }
  },
  {
    "id": "5bce832b1797ff091b693507",
    "status": "active",
    "subject": {
      "entities": [
        {
          "idPattern": "guide_robot.*",
          "type": "guide_robot"
        }
      ],
      "condition": {
        "attrs": [
          "time",
          "r_mode",
          "x",
          "y",
          "theta",
          "r_state"
        ]
      }
    },
    "notification": {
      "timesSent": 1,
      "lastNotification": "2018-10-23T02:10:51.00Z",
      "attrs": [
        "time",
        "r_mode",
        "x",
        "y",
        "theta",
        "r_state"
      ],
      "attrsFormat": "legacy",
      "http": {
        "url": "http://cygnus-elasticsearch:5050/notify"
      }
    }
  }
]
```
