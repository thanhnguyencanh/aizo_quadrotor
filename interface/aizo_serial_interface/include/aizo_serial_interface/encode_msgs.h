#ifndef QUADROTOR_MSGS_ENCODE_MSGS_H
#define QUADROTOR_MSGS_ENCODE_MSGS_H

#include <aizo_planning_msgs/PWMCommand.h>
#include <aizo_planning_msgs/SO3Command.h>
#include <aizo_planning_msgs/TRPYCommand.h>
#include <stdint.h>

#include <vector>

namespace aizo_planning_msgs
{
void encodeSO3Command(const aizo_planning_msgs::SO3Command &so3_command, std::vector<uint8_t> &output);
void encodeTRPYCommand(const aizo_planning_msgs::TRPYCommand &trpy_command, std::vector<uint8_t> &output);
void encodePWMCommand(const aizo_planning_msgs::PWMCommand &pwm_command, std::vector<uint8_t> &output);
}  // namespace aizo_planning_msgs

#endif
