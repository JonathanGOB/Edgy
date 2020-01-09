using System.Collections.Generic;

namespace Modbus
{
    class ConfigDM5
    {

        //Measurement input configuration <description, [0] = adress [1:] = value
        public static readonly Dictionary<string, int> INPUT_SYS = new Dictionary<string, int>(){
            {"adress", 44000},
            {"Single Phase System", 0x00},
            {"two phase system (split phase)", 0x05},
            {"3-wire system, balanced load", 0x01},
            {"3-wire system, balanced load, U=U12 (DM5S only)", 0x11},
            {"3-wire system, balanced load, U=U23 (DM5S only)", 0x21},
            {"3-wire system, balanced load, U=U31 (DM5S only)", 0x31},
            {"3-wire system, unbalanced load", 0x13},
            {"3-wire system, unbalanced load, Aron connection", 0x03},
            {"4-wire system, balanced load", 0x02},
            {"4-wire system, unbalanced load", 0x04},
            {"4-wire system, unbalanced load, Open-Y connection", 0x14}
        };

        //General instantaneous values <description, adress>
        public static readonly Dictionary<string, int> SYSTEM_VOLTAGE = new Dictionary<string, int>(){
            {"System voltage", 40100},
            {"Voltage phase L1 to N", 40102},
            {"Voltage phase L2 to N", 40104},
            {"Voltage phase L3 to N", 40106},
            {"Voltage phase L1 to L2", 40108},
            {"Voltage phase L2 to L3", 40110},
            {"Voltage phase L3 to L1", 40112},
            {"Zero displacement voltage in 4-wire systems", 40114}
        };
    }
}