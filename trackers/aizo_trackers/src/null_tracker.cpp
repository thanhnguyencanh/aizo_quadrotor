#include <aizo_tracker_msgs/TrackerStatus.h>
#include <aizo_trackers_manager/Tracker.h>
#include <ros/ros.h>

class NullTracker : public aizo_trackers_manager::Tracker
{
 public:
  void Initialize(const ros::NodeHandle &nh);
  bool Activate(const aizo_planning_msgs::PositionCommand::ConstPtr &cmd);
  void Deactivate(void);

  aizo_planning_msgs::PositionCommand::ConstPtr update(const nav_msgs::Odometry::ConstPtr &msg);
  uint8_t status() const;
};

void NullTracker::Initialize(const ros::NodeHandle &nh) {}

bool NullTracker::Activate(const aizo_planning_msgs::PositionCommand::ConstPtr &cmd)
{
  return true;
}

void NullTracker::Deactivate(void) {}

aizo_planning_msgs::PositionCommand::ConstPtr NullTracker::update(const nav_msgs::Odometry::ConstPtr &msg)
{
  // Return a null message (will not publish the position command)
  return aizo_planning_msgs::PositionCommand::Ptr();
}

uint8_t NullTracker::status() const
{
  return aizo_tracker_msgs::TrackerStatus::SUCCEEDED;
}

#include <pluginlib/class_list_macros.h>
PLUGINLIB_EXPORT_CLASS(NullTracker, aizo_trackers_manager::Tracker);
