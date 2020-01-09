using System;
using System.IO.Ports;
using EasyModbus;
using System.Collections.Generic;
using Modbus;


namespace Modbus
{
    class Program
    {

        private static string[] ports = new string[] { "COM5" };
        private static List<ModbusClient> clients = new List<ModbusClient>();
        static void Main(string[] args)
        {
            clients = Helpers.setup(ports);
            Console.WriteLine("Value of Discr. Input #1: " + clients[0].ReadHoldingRegisters(20, 4).ToString());	//Reads Discrete Input #1
        }
    }
}
