using System.Collections.Generic;

namespace Modbus {
    class ConfigDM5 {

        //constants for setting up the device
        public static readonly Dictionary<string, int> dict = new Dictionary<string, int>(){
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
    }
}