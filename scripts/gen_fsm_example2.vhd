--! Generated template FSM file for example2 with script proc_graphml.py rev. 0.1
--! File diretory: /mnt/c/Users/User/Desktop/GIT/fsm-yed-vhdl/scripts
--! Generated file name: gen_fsm_example2.vhd from yEd file: example2
--! Date: 2019-05-04 11:38
--! Author: Manuel Mascarenhas





--! FSM state declaration
type t_state_example2 is (failure, idle, start, stop);
--! FSM state instatiation
signal s_state_example2 : t_state_example2;




--! REMEMBER: Do NOT forget to initialize inital state value (at reset for example)! 



--! ####################################################################
--! @brief TODO
--! ####################################################################
case s_state_example2 is
    when failure =>
        --! TODO write your code..
        if state_failure_cond1 then            --! condition: error='0' AND start='1'
        	s_state_example2 <= start
        elsif state_failure_cond2 then            --! c
        	s_state_example2 <= idle
        end if;
    when idle =>
        --! TODO write your code..
        if state_idle_cond1 then            --! condition: d
        	s_state_example2 <= start
        end if;
    when start =>
        --! TODO write your code..
        if state_start_cond1 then            --! condition: b
        	s_state_example2 <= stop
        end if;
    when stop =>
        --! TODO write your code..
        if state_stop_cond1 then            --! condition: 
        	s_state_example2 <= failure
        end if;
    when others =>
end case;