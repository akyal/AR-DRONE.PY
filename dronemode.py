#set mode to guide - this is optional as the goto methd will change the mode if needed.

vehicle.mode = VehicleMode("GUIDED")


#set the target loction in global-relative frame

a_location = LocationGlobalRelative(-34.364114 , 149.166022, 30)
vehicle.simple_goto(a_location)

#set airspeed using attribute
vehicle.airspeed = 5 #m/s

#Set groundspeed using attribute
vehicle.groundspeed = 7.5 #m/s

#set groundspeed using 'simple_goto()' parameter
vehicle.simple_goto(a_location, groundspeed=10)

def send_ned_velocity(velocity_x, velocity_y,velocity_z,duration):
" move vehicle in direction based on specified velocity vectors "

   msg = vehicle.message_factory.set_position_target_local_ned_encode(
                
           0,          #time_boot_ms (not used)

           0, 0,       #target system, target component
                    
                       mavutil.mavlink.MAV_FRAME_LOCAL_NED, #frame

            0b0000111111000111,#type_mask (only speed enabled)
                  0, 0, 0, # x, y, z positions (not used)
          velocity_x, velocity_y, velocity_z, # x ,y,z velocity in m/s
    0, 0, 0, #x, y, z accelerateion(not supported yet, ignored in GCS_Mavlink)
  0, 0)   yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
(not used)
        #send command to vehicle on 1 H z cycle

     for x in range (0, duration):
         vehicle.send_mavlink(msg)
         time.sleep(1)
msg =  vehicle.message_factory.command_long_encode(
           0, 0, # target_system, target_component
  mavutil.mavlink.MAV_CMD_CONDITION_YAW  #command
  0, # confirmation 
   headin,     #param 1, yaw in degrees 
     0,        #param 2, yaw speed deg/s
   1,          #param 3, direction -1 ccw, 1 cw
     is_ relative, #param 4, relative offset 1, absolute angle 0
  0, 0, 0)     # param 5 - 7 not used
#send command to vehicle
vehicle.send_mavlink(msg)

 #set up velocity mappings
 #velocity_x > 0 => fly North
 #velocity_x < 0 => fly South
 #velocity_y > 0 => fly East
 #velocity_y < 0 => fly West
 #velocity_z < 0 => ascend
 #velocity_z > 0 => descend
 SOUTH=-2
 UP=-0.5    #NOTE: up is negative !


#fly south and up.

send_ned_velocity(SOUTH,0,UP, DURATION)
 
  def condition_yaw (heading ,relative= False): 
               if relative: 
                      is_ relative=1 #yw relative to direction of travel
              else: 
                   is_relative=0#yaw is an absolute angle
            #creat the CONDITION_YAW command using_long_encode()
     msg = vehicle.message_factory.command_long_encode(
                 0, 0, # target system, target component
mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command 
                                    0, #confirmation
                                    heading,    #param 1, yaw in degrees
                                    0,          #param 2, yaw speed deg/s
                                    1,          #param 3, direciton -1 ccw, 1 cw
              is_relative, #param 4, relative offset 1, absolute angle 0
                0, 0, 0)   #param 5 ~ 7 not used 
                                               # send command to vehicle
                                            vehicle.send_mavlink(msg)
def set_roi(location):
     #creat the MAV_CMD_DO_SET_ROI command 
msg = vehicle.message_factory.command_long_encode( 
    0, 0, # target system, target component
     mavutil.mavlink.MAV_CMD_DO_SET_ROI, #command
                                 0, #confirmation
                                 0, 0, 0, 0, #params 1-4
                                 location.lat,
                                 location.lon,
                                 location.alt 
                                 )
               #send command to vehicle
              vehicle.send_mavlink(msg)
def get_locaton_metres(original_location, dNorth, dEast):
   earth radius=6378137.0 #Radius of "spherical" earth
       #coordinate offsets in radians
        dLat =dNorth/earth_radius
        dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))
   #New position in decimal degrees
  newlat= original_location.lat +
   (dlat * 180/math.pi)
 newlon = original_location.lon +dlon * 180/math.pi
           if type(original_location) is locationGlobal:
                  targetlocation=LocationGlobal(newlat, newlon, original_location.alt)
        elif type(original_location) is lacationGlobalRelative:
             targetlocation=LocationGlobalRelative(newlat, newlon,original_location.alt) 
          else: 
               raise Exception("invalid location object passed")


          return targetlocation;
      def get_distance_metres(alocation1,alocation2):
                  """
            returns the ground distance in metres between two 'locationGlobal' or 'LocationGlobalRelative' objecs

This method is an approximation, and will not be accurate over large distance and close to the earth's pole.
        """

        dlat = alocation2.lat - alocation1.lat 
        dlong = alocation2.lon - alocation1.lon
      return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5 
def get_bearing(alocation1 , alocation2):

  off_x = alocation2.ion - alocation1.lon
  off_y = alocation2.lat _ alocation.lat
    bearing = 90.00 + math.atan2( off_y, off_x) * 57.2957795
     if bearing < 0:
       bearing += 360.00
    return bearing;




