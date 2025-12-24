#ifndef QUADROTOR_MSGS_DECODE_MSGS_H
#define QUADROTOR_MSGS_DECODE_MSGS_H

#include <aizo_planning_msgs/OutputData.h>
#include <aizo_planning_msgs/StatusData.h>
#include <stdint.h>

#include <vector>

namespace aizo_planning_msgs
{
bool decodeOutputData(const std::vector<uint8_t> &data, aizo_planning_msgs::OutputData &output);

bool decodeStatusData(const std::vector<uint8_t> &data, aizo_planning_msgs::StatusData &status);
}  // namespace aizo_planning_msgs

#endif
