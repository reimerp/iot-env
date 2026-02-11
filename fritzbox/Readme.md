fritztemp2mqtt -> basemqtt
               -> fritzquery
               -> paho

basemqtt -> paho

fritzquery -> fritz

fritzdoc2mqtt -> basemqtt
              -> fritzdoc
              -> paho

fritzdoc -> basemqtt
         -> fritzdata

fritzdata -> fritz
