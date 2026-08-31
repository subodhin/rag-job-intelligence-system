from app.context.database import get_connection


def create_user(user_id: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO users (user_id)
        VALUES (?)
        """,
        (user_id,)
    )

    connection.commit()
    connection.close()


def get_user(user_id: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT user_id
        FROM users
        WHERE user_id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    connection.close()

    if user is None:
        return None

    return {
        "user_id": user[0]
    }

def save_profile(
    user_id: str,
    target_role: str = None,
    experience_level: str = None,
    skills: str = None
):
    create_user(user_id)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO profiles (
            user_id,
            target_role,
            experience_level,
            skills
        )
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            target_role = excluded.target_role,
            experience_level = excluded.experience_level,
            skills = excluded.skills
        """,
        (
            user_id,
            target_role,
            experience_level,
            skills
        )
    )

    connection.commit()
    connection.close()


def get_profile(user_id: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            user_id,
            target_role,
            experience_level,
            skills
        FROM profiles
        WHERE user_id = ?
        """,
        (user_id,)
    )

    profile = cursor.fetchone()

    connection.close()

    if profile is None:
        return None

    return {
        "user_id": profile[0],
        "target_role": profile[1],
        "experience_level": profile[2],
        "skills": profile[3]
    }

def save_preferences(
    user_id: str,
    remote_only: bool = False,
    preferred_locations: str = None,
    preferred_skills: str = None
):
    create_user(user_id)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO preferences (
            user_id,
            remote_only,
            preferred_locations,
            preferred_skills
        )
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            remote_only = excluded.remote_only,
            preferred_locations = excluded.preferred_locations,
            preferred_skills = excluded.preferred_skills
        """,
        (
            user_id,
            int(remote_only),
            preferred_locations,
            preferred_skills
        )
    )

    connection.commit()
    connection.close()


def get_preferences(user_id: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            user_id,
            remote_only,
            preferred_locations,
            preferred_skills
        FROM preferences
        WHERE user_id = ?
        """,
        (user_id,)
    )

    preferences = cursor.fetchone()

    connection.close()

    if preferences is None:
        return None

    return {
        "user_id": preferences[0],
        "remote_only": bool(preferences[1]),
        "preferred_locations": preferences[2],
        "preferred_skills": preferences[3]
    }

def save_message(user_id: str, role: str, content: str):
    create_user(user_id)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO conversation_messages (
            user_id,
            role,
            content
        )
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            role,
            content
        )
    )

    connection.commit()
    connection.close()


def get_conversation(user_id: str, limit: int = 10):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            role,
            content,
            created_at
        FROM conversation_messages
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (
            user_id,
            limit
        )
    )

    messages = cursor.fetchall()

    connection.close()

    messages.reverse()

    return [
        {
            "role": message[0],
            "content": message[1],
            "created_at": message[2]
        }
        for message in messages
    ]


def get_user_context(user_id: str, conversation_limit: int = 10):
    user = get_user(user_id)

    if user is None:
        return None

    profile = get_profile(user_id)
    preferences = get_preferences(user_id)
    conversation = get_conversation(
        user_id,
        limit=conversation_limit
    )

    return {
        "user": user,
        "profile": profile,
        "preferences": preferences,
        "conversation": conversation
    }


def delete_profile(user_id: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM profiles
        WHERE user_id = ?
        """,
        (user_id,)
    )

    connection.commit()
    connection.close()


def delete_preferences(user_id: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM preferences
        WHERE user_id = ?
        """,
        (user_id,)
    )

    connection.commit()
    connection.close()


def delete_conversation(user_id: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM conversation_messages
        WHERE user_id = ?
        """,
        (user_id,)
    )

    connection.commit()
    connection.close()


def delete_user_context(user_id: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM conversation_messages
        WHERE user_id = ?
        """,
        (user_id,)
    )

    cursor.execute(
        """
        DELETE FROM preferences
        WHERE user_id = ?
        """,
        (user_id,)
    )

    cursor.execute(
        """
        DELETE FROM profiles
        WHERE user_id = ?
        """,
        (user_id,)
    )

    connection.commit()
    connection.close()


#for better console read!
def print_user_context(user_context):
    if not user_context:
        print("No user context found.")
        return

    print("\n" + "=" * 60)
    print("                 USER CONTEXT")
    print("=" * 60)

    # User
    user = user_context.get("user", {})

    print("\n[USER]")
    print(f"User ID: {user.get('user_id')}")

    # Profile
    profile = user_context.get("profile", {})

    print("\n[PROFILE]")
    print(f"Target Role:      {profile.get('target_role')}")
    print(f"Experience Level: {profile.get('experience_level')}")
    print(f"Skills:           {profile.get('skills')}")

    # Preferences
    preferences = user_context.get("preferences", {})

    print("\n[PREFERENCES]")
    print(f"Remote Only:          {preferences.get('remote_only')}")
    print(f"Preferred Locations:  {preferences.get('preferred_locations')}")
    print(f"Preferred Skills:     {preferences.get('preferred_skills')}")

    # Conversation
    conversation = user_context.get("conversation", [])

    print("\n[CONVERSATION]")

    if not conversation:
        print("No conversation history.")
    else:
        for i, message in enumerate(conversation, start=1):
            print(f"\n  {i}. {message.get('role', '').upper()}")
            print(f"     {message.get('content', '')}")
            print(f"     Time: {message.get('created_at', '')}")

    print("\n" + "=" * 60)