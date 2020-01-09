using System;
using System.IO.Ports;
using EasyModbus;
using System.Collections.Generic;


namespace Modbus
{
    class Program
    {

        private static string[] ports = new string[] { "COM5" };
        private static List<ModbusClient> clients = new List<ModbusClient>();
        static void Main(string[] args)
        {

            setup();
            ModbusClient modbusClient = new ModbusClient("COM5");
            modbusClient.UnitIdentifier = 0x11;
            modbusClient.Baudrate = 19200;  // Not necessary since default baudrate = 9600
                                            //modbusClient.Parity = System.IO.Ports.Parity.None;
            modbusClient.StopBits = System.IO.Ports.StopBits.One;
            //modbusClient.ConnectionTimeout = 500;			
            modbusClient.Connect();
            Console.WriteLine("Value of Discr. Input #1: " + modbusClient.ReadHoldingRegisters(20, 4).ToString());	//Reads Discrete Input #1
        }

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
        private static List<ModbusClient> setup(string[] ports)
        {

            try
            {
                //initializes the clients and puts them in a list
                List<ModbusClient> clients = new List<ModbusClient>();
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
        private static bool reset(int start, int amount, ModbusClient modbusClient, bool resetValue)
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
