using System;
using System.IO.Ports;
using EasyModbus;
using System.Collections.Generic;

namespace Modbus
{
    class Helpers
    {


        //disconnect all the clients
        public static bool disconnect(List<ModbusClient> clients)
        {
            for (int i = clients.Count; i > 0; i--)
            {
                try
                {
                    clients[i - 1].Disconnect();
                }

                catch (Exception e)
                {
                    Console.WriteLine(e);
                    return false;
                }
            }
            return true;
        }

        //initialize the ports and return modbusclients
        public static List<ModbusClient> setup(string[] ports)
        {

            //initializes the clients and puts them in a list
            List<ModbusClient> clients = new List<ModbusClient>();
            try
            {

                foreach (string port in ports)
                {
                    clients.Add(new ModbusClient(port));
                }

                //setup your clients
                clients[0].UnitIdentifier = 0x11;
                clients[0].Baudrate = 19200;
                clients[0].StopBits = System.IO.Ports.StopBits.One;


                //connects the clients
                foreach (ModbusClient client in clients)
                {
                    client.Connect();
                }
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
            }

            return clients;
        }

        //resets the meters
        public static bool reset(int start, int amount, ModbusClient modbusClient, bool resetValue)
        {
            for (int i = start; start < amount; start++)
            {
                try
                {
                    modbusClient.WriteSingleCoil(start, resetValue);
                }

                catch (Exception e)
                {
                    Console.WriteLine(e);
                    return false;
                }
            }

            return true;
        }
    }
}