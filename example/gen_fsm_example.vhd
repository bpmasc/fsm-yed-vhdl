--! Generated template FSM file for example with script fsm_yed2vhdl.py rev. 0.1
--! File diretory: /mnt/c/Users/User/Desktop/GIT/fsm-yed-vhdl/example
--! Generated file name: gen_fsm_example.vhd from yEd file: example
--! Date: 2019-05-04 11:48
--! Author: Manuel Mascarenhas





--! FSM state declaration
type t_state_example is (failure, idle, run);
--! FSM state instatiation
signal s_state_example : t_state_example;




--! REMEMBER: Do NOT forget to initialize inital state value (at reset for example)! 
s_state_example <= failure;


--! ####################################################################
--! @brief TODO
--! ####################################################################
case s_state_example is
    when failure =>
        --! TODO write your code..
        if state_failure_cond1 then            --! condition: error='0' AND reset='1' AND start='0'
        	s_state_example <= idle
        end if;
    when idle =>
        --! TODO write your code..
        if state_idle_cond1 then            --! condition: start='1' AND error='0'
        	s_state_example <= run
        elsif state_idle_cond2 then            --! condition: error='1'
        	s_state_example <= failure
        end if;
    when run =>
        --! TODO write your code..
        if state_run_cond1 then            --! condition: start='0'AND error='0'
        	s_state_example <= idle
        elsif state_run_cond2 then            --! condition: error='1'
        	s_state_example <= failure
        end if;
    when others =>
end case;