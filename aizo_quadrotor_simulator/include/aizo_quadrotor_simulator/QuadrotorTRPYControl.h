#ifndef QUADROTOR_TRPY_CONTROL_H_
#define QUADROTOR_TRPY_CONTROL_H_

#include <boost/optional.hpp>
#include <aizo_quadrotor_simulator/Quadrotor.h>
#include <aizo_planning_msgs/TRPYCommand.h>

namespace aizo_quadrotor_simulator {
class QuadrotorTRPYControl {
public:
  typedef aizo_planning_msgs::TRPYCommand TRPYCmdMsg;
  void init(const Quadrotor &quad, float I[][3]);
  Quadrotor::MotorState getControl(const Quadrotor::State &state);
  void cmdCallback(const TRPYCmdMsg::ConstPtr &msg);

private:
  float kf_;
  float km_;
  float arm_length_;
  float I_[3][3];
  boost::optional<TRPYCmdMsg> cmd;
};
}
#endif
