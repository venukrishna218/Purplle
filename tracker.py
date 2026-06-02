import uuid

class SessionTracker:
    def __init__(self):
        # Maps raw YOLO track IDs to our stable API visitor metadata
        self.active_sessions = {}

    def process_track(self, track_id: int):
        """
        Takes a raw tracker ID and returns the stable visitor_id.
        Flags if this is a brand new entry vs an existing dwell.
        """
        if track_id not in self.active_sessions:
            # Generate a new unique visitor token for a new session
            self.active_sessions[track_id] = {
                "visitor_id": f"VIS_{uuid.uuid4().hex[:8]}",
                "session_seq": 1,
                "is_new": True
            }
        else:
            # Increment the sequence for existing visitors
            self.active_sessions[track_id]["session_seq"] += 1
            self.active_sessions[track_id]["is_new"] = False

        session_data = self.active_sessions[track_id]
        
        return session_data["visitor_id"], session_data["session_seq"], session_data["is_new"]

    def handle_reentry(self, track_id: int):
        """
        Placeholder for Re-ID logic. If a track is lost and a new one matches 
        historical visual embeddings, merge the IDs to prevent double counting.
        """
        pass