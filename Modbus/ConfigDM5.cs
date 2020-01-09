using System.Collections.Generic;

namespace Modbus
{
    class ConfigDM5
    {

        //Measurement input configuration <description, [0] = adress [1:] = value
        public enum INPUT_SYS
        {
            adress = 44000,
            Single_Phase_System = 0x00,
            two_phase_system_split_phase = 0x05,
            three_wire_system_balanced_load = 0x01,
            three_wire_system_balanced_load_U_U12 = 0x11,
            three_wire_system_balanced_load_U_U2three = 0x21,
            three_wire_system_balanced_load_U_U31 = 0x31,
            three_wire_system_unbalanced_load = 0x13,
            three_wire_system_unbalanced_load_Aron_connection = 0x03,
            four_wire_system_balanced_load = 0x02,
            four_wire_system_unbalanced_load = 0x04,
            four_wire_system_unbalanced_load_Open_Y_connection = 0x14
        };

        //General instantaneous values <description, adress>
        public enum SYSTEM_VOLTAGE
        {
            size_adress = 2,
            system_voltage = 40100,
            voltage_phase_l1_to_n = 40102,
            voltage_phase_l2_to_n = 40104,
            voltage_phase_l3_to_n = 40106,
            voltage_phase_l1_to_l2 = 40108,
            voltage_phase_l2_to_l3 = 40110,
            voltage_phase_l3_to_l1 = 40112,
            zero_displacement_voltage_in_4_wire_systems = 40114

        }
    }
}